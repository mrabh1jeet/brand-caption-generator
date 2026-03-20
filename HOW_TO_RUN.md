# 🚀 HOW TO RUN THE BRAND CAPTION SYSTEM

## 📦 What You Have

Complete full-stack RAG-Enhanced Brand Caption Generation System:
- Flask Backend (Python)
- React Frontend (JavaScript)
- BLIP Image Captioning
- ChromaDB Vector Database
- OpenAI GPT Integration

## 🎯 Quick Start (Choose Your OS)

### Option A: Automated Setup (Recommended)

**Mac/Linux:**
```bash
cd brand-caption-system
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
cd brand-caption-system
setup.bat
```

Then follow the instructions to add your OpenAI API key and run the app.

---

### Option B: Manual Setup

## Step-by-Step Instructions

### 1️⃣ Install Prerequisites

**Install Python 3.8+**
- Mac: `brew install python3`
- Windows: Download from https://www.python.org/downloads/
- Linux: `sudo apt install python3 python3-pip`

**Install Node.js 16+**
- Download from: https://nodejs.org/
- Or use nvm: `nvm install 18`

**Get OpenAI API Key**
- Sign up at: https://platform.openai.com/
- Go to: https://platform.openai.com/api-keys
- Create new key and copy it

### 2️⃣ Setup Backend

```bash
# Navigate to backend folder
cd brand-caption-system/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install Python packages (this may take 5-10 minutes)
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Open .env in any text editor and change:
# OPENAI_API_KEY=your_openai_api_key_here
# to:
# OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx (your actual key)
```

### 3️⃣ Setup Frontend

```bash
# Open a NEW terminal window
# Navigate to frontend folder
cd brand-caption-system/frontend

# Install Node packages (this may take 2-3 minutes)
npm install
```

### 4️⃣ Run the Application

You need TWO terminal windows open:

**Terminal 1 - Run Backend:**
```bash
cd brand-caption-system/backend

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Start Flask server
python app.py

# You should see:
# * Running on http://0.0.0.0:5000
```

**Terminal 2 - Run Frontend:**
```bash
cd brand-caption-system/frontend

# Start React development server
npm start

# Browser should open automatically at http://localhost:3000
```

### 5️⃣ Use the Application

1. **Add Your First Brand**
   - Click "Add New Brand" button
   - Enter brand details:
     - Brand Name: Nike
     - Website URL: https://www.nike.com
     - Instagram Handle: @nike (optional)
   - Click "Add Brand"
   - Wait 30-60 seconds for scraping

2. **Generate a Caption**
   - Select "Nike" from the dropdown
   - Choose personality: "Excitement"
   - Drag & drop an image (or click to upload)
   - Click "Generate Caption"
   - Wait 10-15 seconds
   - Copy the generated caption!

## 🔍 Verify Installation

### Check Backend:
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{"status":"healthy","message":"Brand Caption System API is running"}
```

### Check Frontend:
Open browser to `http://localhost:3000` - you should see the app interface

## 🐛 Troubleshooting

### Backend Issues

**"No module named 'flask'"**
```bash
cd backend
source venv/bin/activate  # Make sure venv is activated
pip install -r requirements.txt
```

**"OpenAI API key not found"**
- Check `backend/.env` file exists
- Make sure it contains: `OPENAI_API_KEY=sk-...`
- Restart the backend after editing .env

**"Port 5000 already in use"**
- Kill the process: `lsof -ti:5000 | xargs kill` (Mac/Linux)
- Or change port in `backend/app.py`: Change 5000 to 5001

### Frontend Issues

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"Cannot find module"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**"Proxy error" or "Network error"**
- Make sure backend is running on port 5000
- Check backend terminal for errors

### Model Loading Issues

**"Out of memory" when loading BLIP**
- The base model is already configured (400MB)
- If still issues, you need at least 4GB RAM
- Close other applications

**"Slow caption generation"**
- First generation takes longer (model loading)
- Subsequent generations are faster
- Consider upgrading to a machine with GPU

## 📊 System Requirements

### Minimum:
- 4GB RAM
- 2 CPU cores
- 5GB disk space
- Internet connection

### Recommended:
- 8GB+ RAM
- 4+ CPU cores
- GPU (optional, for faster inference)
- 10GB disk space

## 🎓 Understanding the System

### File Structure:
```
brand-caption-system/
├── backend/              # Flask API
│   ├── app.py           # Main Flask app
│   ├── services/        # Business logic
│   ├── uploads/         # Temporary image storage
│   └── chroma_db/       # Vector database (created on first run)
│
├── frontend/            # React UI
│   ├── src/
│   │   ├── App.js      # Main component
│   │   └── components/ # UI components
│   └── public/
│
├── README.md           # Full documentation
├── QUICKSTART.md       # Quick reference
└── setup.sh/bat        # Automated setup scripts
```

### How It Works:

1. **Brand Addition:**
   - Scrapes brand website
   - Chunks text into 500-word segments
   - Generates embeddings
   - Stores in ChromaDB vector database

2. **Caption Generation:**
   - BLIP model analyzes image → base caption
   - RAG retrieves relevant brand context
   - GPT synthesizes final caption with hashtags

3. **Technologies:**
   - **BLIP**: Image → Text (Salesforce model)
   - **ChromaDB**: Vector search for brand context
   - **GPT-3.5**: Natural language generation
   - **Flask**: Backend API
   - **React**: Frontend UI

## 💰 Cost Estimates

### OpenAI API Costs:
- GPT-3.5-turbo: ~$0.002 per caption
- 100 captions = ~$0.20
- 1000 captions = ~$2.00

### Upgrading to GPT-4:
- GPT-4: ~$0.03 per caption
- Better quality but 15x more expensive
- To use: Change `self.model = "gpt-4"` in `backend/services/caption_generator.py`

## 🚀 Next Steps

1. **Add More Brands**: Test with 3-5 different brands
2. **Try Different Personalities**: See how tone changes
3. **Experiment with Images**: Different product types
4. **Monitor Costs**: Check OpenAI usage dashboard
5. **Customize**: Modify prompts in `caption_generator.py`

## 📞 Getting Help

**Common Commands:**

Stop servers: `Ctrl+C` in each terminal

Restart backend:
```bash
cd backend
source venv/bin/activate
python app.py
```

Restart frontend:
```bash
cd frontend
npm start
```

Clear database:
```bash
rm -rf backend/chroma_db
# Restart backend to recreate
```

View logs:
- Backend: Look at Terminal 1 output
- Frontend: Open browser console (F12)

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] OpenAI API key obtained
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file created with API key
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000 in browser
- [ ] Added at least one brand
- [ ] Generated at least one caption

## 🎉 You're Ready!

If all checklist items are complete, you have a fully functional RAG-Enhanced Brand Caption Generation System!

Start generating amazing brand-aligned captions for your social media! 🚀
