import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import logging
import os

logger = logging.getLogger(__name__)

class BERTPredictor:
    """BERT-based fake news predictor."""
    
    def __init__(self, model_path="backend/models/distilbert_fake_news"):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.tokenizer = None
        self.max_length = 512
        
    def load_model(self):
        """Load the trained BERT model."""
        try:
            logger.info(f"Loading BERT model from {self.model_path}")
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)
            self.model = DistilBertForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"BERT model loaded successfully on {self.device}")
            return True
        except Exception as e:
            logger.error(f"Error loading BERT model: {e}")
            return False
    
    def predict(self, text: str):
        """
        Predict if news is FAKE or REAL.
        
        Args:
            text: News article text
            
        Returns:
            tuple: (prediction, confidence)
                prediction: "FAKE" or "REAL"
                confidence: float between 0 and 1
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Tokenize
            encoding = self.tokenizer.encode_plus(
                text,
                add_special_tokens=True,
                max_length=self.max_length,
                padding='max_length',
                truncation=True,
                return_attention_mask=True,
                return_tensors='pt'
            )
            
            input_ids = encoding['input_ids'].to(self.device)
            attention_mask = encoding['attention_mask'].to(self.device)
            
            # Predict
            with torch.no_grad():
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
                
                # Get prediction (0=FAKE, 1=REAL)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
                
                prediction = "REAL" if predicted_class == 1 else "FAKE"
                
                logger.info(f"BERT Prediction: {prediction} (confidence: {confidence:.4f})")
                
                return prediction, confidence
                
        except Exception as e:
            logger.error(f"Error during BERT prediction: {e}")
            raise

# Global predictor instance
bert_predictor = None

def get_bert_predictor():
    """Get or create BERT predictor instance."""
    global bert_predictor
    if bert_predictor is None:
        bert_predictor = BERTPredictor()
        if not bert_predictor.load_model():
            logger.warning("Failed to load BERT model, returning None")
            return None
    return bert_predictor
