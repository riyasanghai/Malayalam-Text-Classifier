# Malayalam Text Classifier

A web application that classifies Malayalam text into positive, negative, or neutral sentiment.

## 📁 Essential Files

1. **`flask_app.py`** - Backend server (Python)
2. **`se.html`** - Frontend interface (HTML)
3. **`textclassifier.ipynb`** - ML training notebook (Jupyter)
4. **`malayalam_dataset.csv`** - Dataset (5,211 samples)
5. **`trained_model.pkl`** - Trained XGBoost model (74% accuracy)
6. **`label_encoder.pkl`** - Label encoder
7. **`venv/`** - Python virtual environment
8. **`requirements_flask.txt`** - Python dependencies
9. **`quick_start.sh`** - Quick start script

---

## 🚀 How to Run

### Method 1 - Quick Start:
```bash
cd /Users/riyasanghai/Desktop/project
./quick_start.sh
```

### Method 2 - Manual:
```bash
cd /Users/riyasanghai/Desktop/project
source venv/bin/activate
python flask_app.py
```

Then open `se.html` in your browser.

---

## ✅ Features

- Malayalam text input only (validation included)
- Sentiment: Positive / Negative / Neutral
- 74% accuracy (XGBoost model trained on 5,211 samples)
- Real-time classification without page reload

---

## 🛑 To Stop Server

Press `Ctrl + C` in the terminal window.
