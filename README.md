# 🔍 AI Fake News Detector

An intelligent web application that uses advanced machine learning (BERT) to detect fake news articles with 97% accuracy.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-16.0-black.svg)

## ✨ Features

- 🤖 **BERT-Powered Detection**: Uses DistilBERT transformer model for 97% accuracy
- 🌐 **URL Analysis**: Analyze news from URLs or paste text directly
- 📊 **Sentiment Analysis**: Detects emotional tone and subjectivity
- ✅ **Source Verification**: Cross-references with trusted news sources
- 🔄 **Auto-Correction**: Fixes typos while preserving proper nouns
- 📈 **Confidence Scores**: Shows prediction confidence with visual indicators
- 📜 **History Tracking**: View past analysis results
- ⚡ **Real-time Analysis**: Fast predictions with caching
- 🎨 **Modern UI**: Beautiful, responsive interface with dark mode support

## 🚀 Demo

**Live Demo**: [Coming Soon]

### Screenshots

[Add screenshots here after deployment]

## 🏗️ Tech Stack

### Backend

- **Framework**: FastAPI
- **ML Model**: DistilBERT (Hugging Face Transformers)
- **Fallback Model**: TF-IDF + PassiveAggressiveClassifier
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **APIs**: DuckDuckGo Search, BeautifulSoup for web scraping
- **Features**: Rate limiting, caching, async operations

### Frontend

- **Framework**: Next.js 16 (React)
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React

## 📊 Model Performance

| Model                 | Accuracy | Precision (FAKE) | Precision (REAL) | Speed  |
| --------------------- | -------- | ---------------- | ---------------- | ------ |
| **BERT (Primary)**    | 97.16%   | 98%              | 96%              | ~500ms |
| **TF-IDF (Fallback)** | 94.00%   | 94%              | 94%              | ~50ms  |

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- 2GB+ RAM (for BERT model)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fake-news-detector.git
cd fake-news-detector

# Build and run with Docker Compose
docker-compose up -d --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Option 2: Local Development

**Backend Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"

# Train the BERT model (takes 30-60 mins)
python train_model_bert.py

# Run the backend
uvicorn main:app --reload
```

**Frontend Setup:**

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📖 Usage

### Web Interface

1. Navigate to `http://localhost:3000`
2. Choose input method:
   - **Text**: Paste news article text
   - **URL**: Enter news article URL
3. Click "Analyze News"
4. View results:
   - Prediction (REAL/FAKE)
   - Confidence score
   - Sentiment analysis
   - Source verification
   - Detailed explanation

### API Usage

```bash
# Analyze text
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your news article text here"
  }'

# Analyze URL
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/news-article"
  }'

# Get analysis history
curl "http://localhost:8000/history"
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

## 📁 Project Structure

```
fake-news-detector/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── database.py             # Database configuration
│   ├── train_model_bert.py     # BERT training script
│   ├── services/
│   │   ├── bert_predictor.py   # BERT inference
│   │   ├── scraper.py          # Web scraping
│   │   ├── verifier.py         # Source verification
│   │   ├── sentiment.py        # Sentiment analysis
│   │   ├── corrector.py        # Auto-correction
│   │   └── validator.py        # Input validation
│   ├── tests/                  # Unit tests
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main page
│   │   ├── history/            # History page
│   │   └── components/         # React components
│   ├── package.json            # Node dependencies
│   └── tailwind.config.ts      # Tailwind configuration
└── docker-compose.yml          # Docker configuration
```

## 🔧 Configuration

### Environment Variables

**Backend** (`.env`):

```env
DATABASE_URL=sqlite:///./sql_app.db
MODEL_PATH=backend/models/distilbert_fake_news
```

**Frontend** (`.env.local`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:

- Vercel + Railway
- Render
- Heroku
- AWS
- DigitalOcean

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: [Fake or Real News Dataset](https://github.com/lutzhamel/fake-news)
- **BERT Model**: Hugging Face Transformers
- **Icons**: Lucide React
- **UI Inspiration**: Modern web design trends

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/YOUR_USERNAME/fake-news-detector](https://github.com/YOUR_USERNAME/fake-news-detector)

## 🔮 Future Improvements

- [ ] Multi-language support (Turkish, Spanish, French)
- [ ] Image/video analysis for deepfakes
- [ ] Browser extension
- [ ] Mobile app (React Native)
- [ ] Real-time fact-checking API integration
- [ ] User accounts and saved analyses
- [ ] Social media integration
- [ ] Bias detection
- [ ] Community voting system

---

**⭐ If you find this project useful, please consider giving it a star!**
