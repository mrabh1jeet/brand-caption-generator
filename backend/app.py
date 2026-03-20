from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image

from services.image_captioning import ImageCaptioningService
from services.rag_service import RAGService
from services.caption_generator import CaptionGeneratorService
from services.brand_scraper import BrandScraperService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Initialize services
image_service = ImageCaptioningService()
rag_service = RAGService()
caption_service = CaptionGeneratorService()
scraper_service = BrandScraperService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Brand Caption System API is running'
    })

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get list of available brands in the system"""
    try:
        brands = rag_service.get_available_brands()
        return jsonify({
            'success': True,
            'brands': brands
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/brands/add', methods=['POST'])
def add_brand():
    """Add a new brand by scraping website and social media"""
    try:
        data = request.json
        brand_name = data.get('brand_name')
        website_url = data.get('website_url')
        instagram_handle = data.get('instagram_handle', '')
        
        if not brand_name or not website_url:
            return jsonify({
                'success': False,
                'error': 'Brand name and website URL are required'
            }), 400
        
        # Scrape brand content
        result = scraper_service.scrape_brand(
            brand_name=brand_name,
            website_url=website_url,
            instagram_handle=instagram_handle
        )
        
        # Add to RAG knowledge base
        rag_service.add_brand_documents(brand_name, result['documents'])
        
        return jsonify({
            'success': True,
            'message': f'Brand {brand_name} added successfully',
            'documents_added': len(result['documents'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/caption/generate', methods=['POST'])
def generate_caption():
    """Generate brand-aligned caption from image"""
    try:
        # Check if image is provided
        if 'image' not in request.files and 'image_base64' not in request.form:
            return jsonify({
                'success': False,
                'error': 'No image provided'
            }), 400
        
        # Get parameters
        brand_name = request.form.get('brand_name')
        personality = request.form.get('personality', 'excitement')
        
        if not brand_name:
            return jsonify({
                'success': False,
                'error': 'Brand name is required'
            }), 400
        
        # Process image
        if 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No selected file'
                }), 400
            
            if not allowed_file(file.filename):
                return jsonify({
                    'success': False,
                    'error': 'File type not allowed'
                }), 400
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = filepath
        else:
            # Handle base64 image
            image_data = request.form.get('image_base64')
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(BytesIO(image_bytes))
            
            # Save temporarily
            filename = 'temp_image.png'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_path = filepath
        
        # Step 1: Generate base caption from image
        base_caption = image_service.generate_caption(image_path)
        
        # Step 2: Retrieve relevant brand context
        brand_context = rag_service.retrieve_brand_context(
            brand_name=brand_name,
            query=base_caption,
            personality=personality,
            top_k=5
        )
        
        # Step 3: Generate final caption
        final_caption = caption_service.generate_caption(
            base_caption=base_caption,
            brand_context=brand_context,
            brand_name=brand_name,
            personality=personality
        )
        
        # Clean up temporary file
        if os.path.exists(image_path):
            os.remove(image_path)
        
        return jsonify({
            'success': True,
            'base_caption': base_caption,
            'final_caption': final_caption['caption'],
            'hashtags': final_caption['hashtags'],
            'mentions': final_caption['mentions']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/caption/generate-text', methods=['POST'])
def generate_caption_from_text():
    """Generate caption from text description (no image)"""
    try:
        data = request.json
        description = data.get('description')
        brand_name = data.get('brand_name')
        personality = data.get('personality', 'excitement')
        
        if not description or not brand_name:
            return jsonify({
                'success': False,
                'error': 'Description and brand name are required'
            }), 400
        
        # Retrieve brand context
        brand_context = rag_service.retrieve_brand_context(
            brand_name=brand_name,
            query=description,
            personality=personality,
            top_k=5
        )
        
        # Generate caption
        final_caption = caption_service.generate_caption(
            base_caption=description,
            brand_context=brand_context,
            brand_name=brand_name,
            personality=personality
        )
        
        return jsonify({
            'success': True,
            'final_caption': final_caption['caption'],
            'hashtags': final_caption['hashtags'],
            'mentions': final_caption['mentions']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
