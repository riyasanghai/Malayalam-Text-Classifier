#!/bin/bash

echo "=========================================="
echo "🚀 Malayalam Text Classifier - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️ Virtual environment not found. Please ensure venv/ folder exists."
    exit 1
fi

echo "✅ Virtual environment found"
echo ""

echo "=========================================="
echo "🚀 Starting Flask Backend Server..."
echo "=========================================="
echo ""
echo "📍 Server: http://127.0.0.1:8000"
echo "🌐 Next: Open se.html in your browser"
echo "⚡ Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Activate virtual environment and start Flask server
source venv/bin/activate
python flask_app.py
