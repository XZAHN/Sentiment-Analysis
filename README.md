# Sentiment Prediction System

A machine learning system for sentiment analysis with a ChatGPT-like dark theme interface.

## Setup

1. **Train the model:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python train.py
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Features

- Dark theme interface similar to ChatGPT
- Real-time sentiment analysis (positive/negative)
- Conversational UI
- REST API endpoint for predictions

## API

### POST /predict
Predict sentiment of text.

**Request:**
```json
{
  "text": "I love this movie!"
}
```

**Response:**
```json
{
  "sentiment": 1  // 1 for positive, 0 for negative
}
```