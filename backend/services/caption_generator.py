import os
import re

try:
    from google import genai
    from google.genai import types
    USE_NEW_API = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_API = False

class CaptionGeneratorService:
    def __init__(self):
        """Initialize Google Gemini client"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("WARNING: GEMINI_API_KEY not set. Caption generation will fail.")
        
        if USE_NEW_API:
            # New API
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-3-flash-preview'
        else:
            # Old API (deprecated but still works)
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemini-3-flash-preview')
    
    def generate_caption(self, base_caption, brand_context, brand_name, personality):
        """
        Generate final Instagram caption using Gemini
        
        Args:
            base_caption: Base image caption
            brand_context: Retrieved brand documents
            brand_name: Name of the brand
            personality: Brand personality
            
        Returns:
            dict: Generated caption with hashtags and mentions
        """
        try:
            # Build context from retrieved documents
            context_text = "\n".join(brand_context[:3]) if brand_context else "No specific brand context available."
            
            # Create prompt
            prompt = f"""You are a social media expert creating Instagram captions for {brand_name}.

Brand Personality: {personality}

Image Description: {base_caption}

Brand Context:
{context_text}

Task: Generate an engaging Instagram caption that:
1. Reflects the {personality} personality
2. Is aligned with {brand_name}'s brand voice
3. Includes 2-4 relevant hashtags
4. Is concise and catchy (max 150 characters)
5. Uses emojis sparingly if appropriate

Output format:
Caption: [your caption here]
Hashtags: #tag1 #tag2 #tag3
Mentions: @mention1 @mention2 (if relevant, otherwise leave empty)
"""

            # Call Gemini API
            if USE_NEW_API:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                output = response.text
            else:
                response = self.model.generate_content(prompt)
                output = response.text
            
            # Parse response
            caption, hashtags, mentions = self._parse_output(output)
            
            return {
                'caption': caption,
                'hashtags': hashtags,
                'mentions': mentions
            }
        
        except Exception as e:
            print(f"Error generating caption: {str(e)}")
            # Fallback caption
            return {
                'caption': f"{base_caption} #{brand_name}",
                'hashtags': [f"#{brand_name}"],
                'mentions': []
            }
    
    def _parse_output(self, output):
        """Parse Gemini output to extract caption, hashtags, and mentions"""
        caption = ""
        hashtags = []
        mentions = []
        
        try:
            lines = output.strip().split('\n')
            
            for line in lines:
                if line.startswith('Caption:'):
                    caption = line.replace('Caption:', '').strip()
                elif line.startswith('Hashtags:'):
                    hashtag_text = line.replace('Hashtags:', '').strip()
                    hashtags = re.findall(r'#\w+', hashtag_text)
                elif line.startswith('Mentions:'):
                    mention_text = line.replace('Mentions:', '').strip()
                    mentions = re.findall(r'@\w+', mention_text)
            
            # If caption is empty, use the full output
            if not caption:
                caption = output.strip()
        
        except Exception as e:
            print(f"Error parsing output: {str(e)}")
            caption = output.strip()
        
        return caption, hashtags, mentions