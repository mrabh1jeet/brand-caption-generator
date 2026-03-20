#!/bin/bash

echo "🚀 Setting up Brand Caption Generation System..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

echo "✓ Python and Node.js found"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
fi

cd ..

echo "✓ Backend setup complete"
echo ""

# Setup Frontend
echo "📦 Setting up Frontend..."
cd frontend

npm install

cd ..

echo "✓ Frontend setup complete"
echo ""

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "⚠️  Don't forget to add your OPENAI_API_KEY to backend/.env"
