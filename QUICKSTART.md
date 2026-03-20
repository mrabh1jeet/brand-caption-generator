# Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- OpenAI API Key (get from https://platform.openai.com/api-keys)

### 2. One-Command Setup

**Mac/Linux:**
```bash
chmod +x setup.sh && ./setup.sh
```

**Windows:**
```bash
setup.bat
```

### 3. Add API Key

Edit `backend/.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 5. Open Browser

Navigate to: `http://localhost:3000`

## 🎯 First Use

1. **Add a Brand** (e.g., Nike)
   - Brand Name: `Nike`
   - Website: `https://www.nike.com`
   - Click "Add Brand"
   - Wait 30 seconds for scraping

2. **Generate Caption**
   - Select "Nike" from dropdown
   - Choose personality: "Excitement"
   - Upload a shoe image
   - Click "Generate Caption"
   - Copy the result!

## 🔧 Configuration

### Use GPT-4 (Better Quality)
In `backend/services/caption_generator.py`:
```python
self.model = "gpt-4"  # Change from gpt-3.5-turbo
```

### Reduce Memory Usage
In `backend/services/image_captioning.py`, keep the base model:
```python
# Already using base model - no changes needed
```

### Add More Brands Programmatically
```python
import requests

requests.post('http://localhost:5000/api/brands/add', json={
    'brand_name': 'Apple',
    'website_url': 'https://www.apple.com',
    'instagram_handle': '@apple'
})
```

## 🐛 Common Issues

### "Module not found"
```bash
cd backend
pip install -r requirements.txt
```

### "OpenAI API Error"
- Check your API key in `backend/.env`
- Verify billing is set up at https://platform.openai.com

### "Port already in use"
Change port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### CORS Issues
Make sure Flask is running on port 5000 or update proxy in `frontend/package.json`

## 📊 Testing

Test backend API:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status":"healthy","message":"Brand Caption System API is running"}
```

## 🚀 Deployment

### Backend (Flask)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (React)
```bash
npm run build
# Serve the build folder with nginx or similar
```

## 📞 Support

Issues? Check:
1. README.md - Detailed documentation
2. Backend logs in terminal 1
3. Browser console (F12) for frontend errors

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com
- **React**: https://react.dev
- **ChromaDB**: https://docs.trychroma.com
- **BLIP**: https://huggingface.co/Salesforce/blip-image-captioning-base
- **OpenAI API**: https://platform.openai.com/docs
