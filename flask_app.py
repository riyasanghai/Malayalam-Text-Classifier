"""
Flask Backend for Malayalam Text Classifier
Simple implementation that works with your existing HTML frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
from textblob import TextBlob
import re
import pickle
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests from HTML frontend

# Initialize classifier (will be loaded on first request)
classifier = None
embedding_model = None
label_encoder = None

def is_malayalam_text(text):
    """Check if text contains Malayalam characters"""
    # Malayalam Unicode range: U+0D00 to U+0D7F
    malayalam_chars = re.findall(r'[\u0D00-\u0D7F]', text)
    total_chars = re.findall(r'[^\s\W\d]', text)  # All letter characters excluding spaces, punctuation, digits
    
    if len(total_chars) == 0:
        return False
    
    # At least 50% of the characters should be Malayalam
    malayalam_ratio = len(malayalam_chars) / len(total_chars)
    return malayalam_ratio >= 0.5

def clean_text(text):
    """Clean and preprocess Malayalam text"""
    text = str(text).strip()
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'[@#]\w+', '', text)  # Remove mentions/hashtags
    text = re.sub(r'[^\w\s\u0D00-\u0D7F]', ' ', text)  # Keep Malayalam chars
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def translate_malayalam_to_english(text):
    """Translate Malayalam text to English"""
    try:
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def simple_sentiment_classification(text):
    """
    Simple rule-based sentiment classification
    Uses TextBlob for sentiment analysis
    """
    try:
        # Analyze sentiment using TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Classify based on polarity
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Classification error: {e}")
        return "neutral"

def advanced_sentiment_classification(text):
    """
    Advanced classification using pre-trained model
    Falls back to simple classification if model not available
    """
    global classifier, embedding_model, label_encoder
    
    try:
        # Load models if not already loaded
        if classifier is None or embedding_model is None:
            from sentence_transformers import SentenceTransformer
            import pickle
            
            # Check for saved model
            if os.path.exists('trained_model.pkl') and os.path.exists('label_encoder.pkl'):
                print("📦 Loading pre-trained model...")
                with open('trained_model.pkl', 'rb') as f:
                    classifier = pickle.load(f)
                with open('label_encoder.pkl', 'rb') as f:
                    label_encoder = pickle.load(f)
                embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
                print("✅ Models loaded successfully!")
            else:
                print("⚠️ Pre-trained model not found. Using simple classification.")
                return simple_sentiment_classification(text)
        
        # Generate embedding and predict (runs every time)
        embedding = embedding_model.encode([text], convert_to_numpy=True, normalize_embeddings=True)
        prediction = classifier.predict(embedding)[0]
        sentiment = label_encoder.inverse_transform([prediction])[0]
        return sentiment
        
    except Exception as e:
        print(f"⚠️ Advanced model error: {e}. Using simple classification.")
        return simple_sentiment_classification(text)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "status": "running",
        "message": "Malayalam Text Classifier API",
        "endpoints": {
            "/classify": "POST - Classify Malayalam text sentiment"
        }
    })

@app.route('/classify', methods=['POST'])
def classify_text():
    """
    Main classification endpoint
    Receives text from frontend and returns sentiment
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        user_text = data['text'].strip()
        
        if not user_text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Validate Malayalam text
        if not is_malayalam_text(user_text):
            print(f"⚠️ Non-Malayalam text detected: {user_text[:50]}...")
            return jsonify({"error": "Please enter text in Malayalam only. മലയാളത്തിൽ മാത്രം ടൈപ്പ് ചെയ്യുക."}), 400
        
        print(f"\n📝 Received: {user_text[:100]}...")
        
        # Step 1: Clean text
        cleaned_text = clean_text(user_text)
        
        # Step 2: Translate to English
        english_text = translate_malayalam_to_english(cleaned_text)
        print(f"🔄 Translated: {english_text[:100]}...")
        
        # Step 3: Classify sentiment
        sentiment = advanced_sentiment_classification(english_text)
        print(f"✅ Predicted Sentiment: {sentiment}\n")
        
        # Return result
        return jsonify({
            "label": sentiment,
            "original_text": user_text,
            "translated_text": english_text
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": f"Classification failed: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": classifier is not None
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Malayalam Text Classifier - Flask Backend Server")
    print("="*60)
    print("📍 Server URL: http://127.0.0.1:8000")
    print("🌐 Open 'se.html' in your browser to use the application")
    print("📚 API Endpoints:")
    print("   - GET  /         : Server info")
    print("   - POST /classify : Classify text sentiment")
    print("   - GET  /health   : Health check")
    print("="*60)
    print("⚡ Server is running... Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Run Flask server
    app.run(host='127.0.0.1', port=8000, debug=False)
