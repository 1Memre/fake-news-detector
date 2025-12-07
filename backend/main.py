import logging
import os
import joblib
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Absolute imports assuming running from package root or inside docker /app
# If these fail, we might need relative imports, but standard generic imports are safer for app entry points.
try:
    import models
    import database
    from services import scraper, verifier, sentiment, validator, corrector, bert_predictor
except ImportError:
    # Fallback for running from parent directory
    from . import models, database
    from .services import scraper, verifier, sentiment, validator, corrector, bert_predictor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Setup Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Global model variables
ml_model = None  # Old TF-IDF model (fallback)
bert_model = None  # BERT model (primary)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    global ml_model, bert_model
    
    # Try to load BERT model first (primary)
    try:
        logger.info("Loading BERT model...")
        bert_model = bert_predictor.get_bert_predictor()
        if bert_model:
            logger.info("✅ BERT model loaded successfully (primary model)")
        else:
            logger.warning("⚠️ BERT model failed to load, will use TF-IDF as fallback")
    except Exception as e:
        logger.error(f"Error loading BERT model: {e}")
        logger.info("Will use TF-IDF model as fallback")
    
    # Load TF-IDF model as fallback
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "fake_news_model.pkl")
        
        if os.path.exists(model_path):
            ml_model = joblib.load(model_path)
            logger.info(f"✅ TF-IDF model loaded successfully (fallback model)")
        else:
            alt_path = "backend/fake_news_model.pkl"
            if os.path.exists(alt_path):
                ml_model = joblib.load(alt_path)
                logger.info(f"✅ TF-IDF model loaded from {alt_path}")
            else:
                logger.error(f"❌ TF-IDF model not found")
    except Exception as e:
        logger.error(f"Error loading TF-IDF model: {e}")
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down API")

app = FastAPI(title="AI Fake News Detector API", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Models ---
class NewsRequest(BaseModel):
    text: str = ""
    url: str | None = None

class Source(BaseModel):
    domain: str
    url: str
    title: str = ""

class Correction(BaseModel):
    domain: str
    url: str
    title: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: str
    sources: List[Source] = []
    explanation: str = ""
    correction: Correction | None = None
    sentiment_score: float = 0.0
    sentiment_label: str = "Neutral"
    subjectivity_score: float = 0.0
    original_text: str | None = None
    corrected_text: str | None = None

# --- Endpoints ---

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Fake News Detector API"}

@app.post("/predict", response_model=PredictionResponse)
@limiter.limit("20/minute")
async def predict_news(request: Request, news_request: NewsRequest, db: Session = Depends(get_db)):
    """
    Main prediction endpoint.
    Orchestrates validation, scraping, prediction, verification, and explanation.
    """
    input_text = news_request.text
    
    # 0. Check for URL and Scrape if needed
    if news_request.url and (not input_text or len(input_text) < 50):
        logger.info(f"Extracting text from URL: {news_request.url}")
        extracted_text = await scraper.extract_text_from_url(news_request.url)
        if extracted_text:
            input_text = extracted_text
        else:
            # Return early if scraping failed
            return PredictionResponse(
                prediction="INVALID",
                confidence="N/A",
                explanation="Could not extract text from the provided URL. Please paste the text manually."
            )

    # 1. Validate Input
    validation_error = validator.validate_input(input_text)
    if validation_error:
        return PredictionResponse(
            prediction="INVALID",
            confidence="N/A",
            explanation=validation_error
        )
        
    # 2. Auto-Correction
    original_text = input_text
    corrected_text = corrector.correct_text(input_text)
    # Use corrected text for analysis if it changed significantly (you can add threshold logic here if needed)
    input_text = corrected_text

    # 3. Get AI Prediction
    try:
        # Try BERT model first (primary)
        if bert_model:
            logger.info("Using BERT model for prediction")
            prediction_result, confidence = bert_model.predict(input_text)
            confidence_str = f"{confidence * 100:.1f}%"
        # Fallback to TF-IDF model
        elif ml_model:
            logger.info("Using TF-IDF model for prediction (BERT not available)")
            prediction_result = ml_model.predict([input_text])[0]
            proba = ml_model.predict_proba([input_text])[0]
            confidence = max(proba) * 100
            confidence_str = f"{confidence:.1f}%"
        else:
            raise HTTPException(status_code=503, detail="No model loaded")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
    
    # 3. Verify Sources (Async)
    # Run source verification concurrently if possible, but here we await it
    sources_data = await verifier.verify_sources(input_text)
    
    # Map raw sources to Pydantic models
    sources_model = [Source(**s) for s in sources_data]
    
    # Hybrid Logic: If trusted sources are found, override the model
    if sources_model:
        prediction_result = "REAL"
        confidence_str = "100% (Verified Source)"
        
    # 4. Generate Explanation (Sync)
    # Using the raw list of sources for logic
    explanation_text = verifier.generate_explanation(input_text, prediction_result, sources_data)
    
    # 7. Get Correction if FAKE (Async)
    correction_model = None
    if prediction_result == "FAKE":
        correction_data = await verifier.get_correction(input_text)
        if correction_data:
            correction_model = Correction(**correction_data)
        
    # 8. Sentiment Analysis (Sync)
    polarity, subjectivity, sentiment_label = sentiment.analyze_sentiment(input_text)
    
    # 9. Save to Database (Sync)
    try:
        db_prediction = models.Prediction(
            text=input_text, 
            prediction=prediction_result,
            confidence=confidence_str
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
    except Exception as e:
        logger.error(f"Database error: {e}")
        # Don't fail the request if DB logging fails
    
    return PredictionResponse(
        prediction=prediction_result, 
        confidence=confidence_str,
        sources=sources_model,
        explanation=explanation_text,
        correction=correction_model,
        sentiment_score=polarity,
        sentiment_label=sentiment_label,
        subjectivity_score=subjectivity,
        original_text=original_text if original_text != corrected_text else None,
        corrected_text=corrected_text if original_text != corrected_text else None
    )

@app.get("/history")
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Keep this sync for now as DB operations are blocking with Session
    # In a full async app, we'd use AsyncSession
    predictions = db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).offset(skip).limit(limit).all()
    return predictions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
