#!/bin/bash

echo "=========================================="
echo "FIXING MAC SSL AND INSTALLING PACKAGES"
echo "=========================================="
echo ""

# Fix Mac SSL Certificate Issues
echo "Step 1: Fixing SSL certificates..."

# Option 1: Install certificates from Python
if [ -f "/Applications/Python 3.13/Install Certificates.command" ]; then
    echo "Running Python 3.13 certificate installer..."
    "/Applications/Python 3.13/Install Certificates.command"
elif [ -f "/Applications/Python 3.10/Install Certificates.command" ]; then
    echo "Running Python 3.10 certificate installer..."
    "/Applications/Python 3.10/Install Certificates.command"
fi

# Option 2: Install certifi
pip install --upgrade certifi

echo ""
echo "Step 2: Installing required packages..."
echo ""

# Install packages one by one
echo "Installing Flask..."
pip install flask flask-cors python-dotenv

echo "Installing Google Gemini (new API)..."
pip install google-genai

echo "Installing Google Gemini (old API - fallback)..."
pip install google-generativeai

echo "Installing data processing..."
pip install requests beautifulsoup4 Pillow

echo "Installing AI packages..."
pip install sentence-transformers chromadb

echo ""
echo "=========================================="
echo "INSTALLATION COMPLETE!"
echo "=========================================="
echo ""
echo "Now run:"
echo "  python app.py"