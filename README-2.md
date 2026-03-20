# RAG-Enhanced Brand Caption Generation System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> AI-powered social media caption generation system that creates brand-aligned, personality-driven Instagram captions using Retrieval-Augmented Generation (RAG) and Vision Language Models.

## 📖 Overview

This system enables zero-shot brand-aligned caption generation for social media marketing without requiring brand-specific fine-tuning. By combining Google's Gemini Vision for image understanding with a RAG architecture for brand knowledge retrieval, it generates captions that match specific brand personalities across five dimensions: Sincerity, Excitement, Competence, Sophistication, and Ruggedness.

### Key Features

- 🎯 **Zero-shot Brand Adaptation**: No training data required - just provide a brand website
- 🎨 **Personality-Driven Generation**: 5 brand personality dimensions (Aaker's framework)
- ⚡ **Real-time Performance**: ~12 seconds per caption, ~45 seconds brand onboarding
- 🔍 **RAG Architecture**: Dynamic brand knowledge retrieval from vector database
- 📊 **Production-Ready**: Flask REST API + React frontend

### Research Results

- **CLIPScore**: 0.87 (image-caption alignment)
- **Brand Alignment**: 4.2/5 (human evaluation)
- **17% improvement** over baseline methods
- **70% reduction** in caption creation time

## 🏗️ Architecture

The system consists of two main pipelines:

### Pipeline 1: Knowledge Base Creation (Offline)
```
Brand Website → Web Scraper → Text Chunking → Embeddings → Vector DB
```

### Pipeline 2: Caption Generation (Online)
```
Product Image → Vision Model → RAG Retrieval → LLM → Brand Caption + Hashtags
```

![System Architecture](docs/architecture.png)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 14+ (for React frontend)
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/brand-caption-generator.git
cd brand-caption-generator
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
CHROMA_PERSIST_DIR=./chroma_db
EOF
```

3. **Frontend Setup**
```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Open http://localhost:3000 in your browser! 🎉

## 📚 Usage

### 1. Add a Brand

Click **"+ Add New Brand"** and provide:
- Brand name (e.g., "Nike")
- Website URL (e.g., "https://www.nike.com")

The system will automatically scrape and index brand content (~45 seconds).

### 2. Generate Caption

1. Select a brand from the dropdown
2. Choose a personality (Excitement, Sincerity, Competence, Sophistication, Ruggedness)
3. Upload a product image
4. Click **"Generate Caption"**

Results include:
- Base caption (image description)
- Final brand-aligned caption
- Relevant hashtags
- Brand mentions (if applicable)

### 3. Examples

**Same Nike Dunk Image, Different Personalities:**

| Personality | Generated Caption |
|-------------|-------------------|
| Excitement | "Fresh drop! 🚀 These kicks are pure energy..." |
| Sincerity | "True to the original. The Dunk High honors heritage..." |
| Competence | "Built for precision. Excellence in motion..." |
| Sophistication | "Refined by heritage. A masterclass in contrast..." |
| Ruggedness | "Hardwood heritage, concrete grit. Built to endure..." |

## 🔧 API Reference

### Add Brand
```bash
POST /api/brands/add
Content-Type: application/json

{
  "brand_name": "Nike",
  "website_url": "https://www.nike.com"
}
```

### Generate Caption
```bash
POST /api/caption/generate
Content-Type: multipart/form-data

{
  "image": <file>,
  "brand_name": "Nike",
  "personality": "excitement"
}
```

### List Brands
```bash
GET /api/brands
```

## 🧪 Testing

Run automated test suite:

```bash
cd backend
source venv/bin/activate

# Run all tests
python test_automated.py

# Calculate CLIPScore
python test_clipscore.py test_results/test_results_*.json

# Generate human evaluation survey
python test_human_eval.py test_results/test_results_*.json
```

See [TESTING_GUIDE.md](backend/TESTING_GUIDE.md) for comprehensive testing documentation.

## 📊 Project Structure

```
brand-caption-generator/
├── backend/
│   ├── app.py                      # Flask REST API
│   ├── services/
│   │   ├── image_captioning.py     # Gemini Vision integration
│   │   ├── caption_generator.py    # Brand-aligned generation
│   │   ├── rag_service.py          # RAG retrieval logic
│   │   └── brand_scraper.py        # Web scraping
│   ├── chroma_db/                  # Vector database (auto-created)
│   ├── uploads/                    # Uploaded images (auto-created)
│   ├── requirements.txt            # Python dependencies
│   ├── test_automated.py           # Automated test suite
│   ├── test_clipscore.py           # CLIPScore evaluation
│   └── view_chromadb.py            # Database viewer tool
├── frontend/
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   ├── components/
│   │   │   ├── BrandSelector.js    # Brand dropdown
│   │   │   ├── ImageUpload.js      # Image upload UI
│   │   │   ├── CaptionDisplay.js   # Results display
│   │   │   └── AddBrand.js         # Brand addition modal
│   │   └── App.css                 # Styling
│   ├── package.json                # Node dependencies
│   └── public/
├── docs/
│   ├── architecture.png            # System diagram
│   └── IEEE_Paper.pdf              # Research paper
├── README.md
├── LICENSE
└── .gitignore
```

## 🛠️ Technology Stack

**Backend:**
- Flask (Python web framework)
- Google Gemini 3 Flash (Vision & LLM)
- ChromaDB (Vector database)
- sentence-transformers (Embeddings)
- BeautifulSoup (Web scraping)

**Frontend:**
- React 18.2
- Axios (HTTP client)
- CSS3 (Styling)

**Key Libraries:**
- `transformers`: For CLIP evaluation
- `requests`: API calls
- `Pillow`: Image processing
- `python-dotenv`: Environment management

## 📈 Performance

| Metric | Value |
|--------|-------|
| Brand Onboarding | 45 ± 12s |
| Caption Generation | 12 ± 3s |
| RAG Retrieval | 0.8 ± 0.2s |
| CLIPScore | 0.87 ± 0.05 |
| Human Preference | 75% |



## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🐛 Troubleshooting

### Common Issues

**Issue: "GEMINI_API_KEY not found"**
```bash
# Make sure .env file exists in backend/
cd backend
echo "GEMINI_API_KEY=your_key_here" > .env
```

**Issue: "Port 5000 already in use"**
```bash
# macOS AirPlay uses port 5000
# Either disable AirPlay or change port in backend/app.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

**Issue: "SSL Certificate Error"**
```bash
# Run the certificate installer
/Applications/Python\ 3.*/Install\ Certificates.command
pip install --upgrade certifi
```

**Issue: "Module not found"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 📧 Contact

Your Name - abhijeetkumar28303@gmail.com

Project Link: [https://github.com/mrabh1jeet/brand-caption-generator](https://github.com/yourusername/brand-caption-generator)

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) for the Vision and LLM APIs
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [Sentence Transformers](https://www.sbert.net/) for embedding models
- [Aaker's Brand Personality Framework](https://en.wikipedia.org/wiki/Brand_personality) for theoretical foundation

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Additional social media platforms (Twitter, LinkedIn, TikTok)
- [ ] Campaign-aware generation
- [ ] A/B testing integration
- [ ] Fine-tuning capabilities
- [ ] Brand logo detection
- [ ] Multi-image carousel captions
- [ ] Video caption generation

---

**Made with ❤️ for better social media marketing**
