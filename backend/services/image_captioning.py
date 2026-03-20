from PIL import Image
import os

class ImageCaptioningService:
    def __init__(self):
        """Initialize Gemini Vision for image captioning"""
        print("Initializing Image Captioning Service...")
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("ERROR: GEMINI_API_KEY not found!")
            self.model = None
            return
        
        try:
            # Use the stable legacy API
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Use Gemini 3 Flash Preview - the latest and most advanced model
            model_name = 'models/gemini-3-flash-preview'
            
            self.model = genai.GenerativeModel(model_name)
            print(f"✓ Image Captioning initialized with: {model_name}")
            self.model_name = model_name
            
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            self.model = None
    
    def generate_caption(self, image_path):
        """
        Generate caption from image using Gemini Vision
        
        Args:
            image_path: Path to image file
            
        Returns:
            str: Generated caption
        """
        if not self.model:
            print("⚠ Model not initialized! Using fallback")
            return self._get_simple_description(image_path)
        
        try:
            print(f"📸 Generating caption for: {image_path}")
            
            # Load image using PIL
            image = Image.open(image_path).convert('RGB')
            
            # Create detailed prompt
            prompt = """Describe this image in 2-3 concise sentences. Include:
- The main product or subject
- Key colors and visual style
- Notable features or details

Be specific and descriptive for social media."""
            
            # Generate content with image
            response = self.model.generate_content([prompt, image])
            
            if response and hasattr(response, 'text') and response.text:
                caption = response.text.strip()
                print(f"✓ Generated: {caption[:100]}...")
                return caption
            else:
                print("⚠ No text in response")
                return self._get_simple_description(image_path)
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error: {error_msg[:200]}")
            
            # Check for specific errors
            if "404" in error_msg or "not found" in error_msg.lower():
                print("Model not available. Using simple description.")
            elif "quota" in error_msg.lower():
                print("API quota exceeded!")
            elif "api key" in error_msg.lower():
                print("API key issue!")
            
            return self._get_simple_description(image_path)
    
    def _get_simple_description(self, image_path):
        """Generate a basic description when vision fails"""
        try:
            image = Image.open(image_path)
            width, height = image.size
            
            # Try to guess content type from filename
            filename = os.path.basename(image_path).lower()
            
            if any(x in filename for x in ['shoe', 'sneaker', 'boot']):
                return f"a stylish footwear product ({width}x{height})"
            elif any(x in filename for x in ['phone', 'iphone', 'mobile']):
                return f"a sleek smartphone device ({width}x{height})"
            elif any(x in filename for x in ['laptop', 'macbook', 'computer']):
                return f"a modern laptop computer ({width}x{height})"
            elif any(x in filename for x in ['watch', 'clock']):
                return f"an elegant timepiece ({width}x{height})"
            else:
                return f"a premium product showcased in high quality ({width}x{height})"
        except:
            return "a product image"