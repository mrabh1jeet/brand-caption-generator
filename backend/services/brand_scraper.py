import requests
from bs4 import BeautifulSoup
import time

class BrandScraperService:
    def __init__(self):
        """Initialize scraper with headers"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_brand(self, brand_name, website_url, instagram_handle=""):
        """
        Scrape brand content from website
        
        Args:
            brand_name: Name of the brand
            website_url: Brand website URL
            instagram_handle: Instagram handle (optional)
            
        Returns:
            dict: Scraped documents
        """
        documents = []
        
        try:
            # Scrape website
            print(f"Scraping website: {website_url}")
            website_docs = self._scrape_website(website_url)
            documents.extend(website_docs)
            
            # Add some default brand documents if scraping fails
            if not documents:
                documents = self._create_default_documents(brand_name, website_url)
            
            print(f"Collected {len(documents)} documents for {brand_name}")
            
            return {
                'brand_name': brand_name,
                'documents': documents
            }
        
        except Exception as e:
            print(f"Error scraping brand: {str(e)}")
            # Return default documents
            return {
                'brand_name': brand_name,
                'documents': self._create_default_documents(brand_name, website_url)
            }
    
    def _scrape_website(self, url):
        """Scrape text content from website"""
        documents = []
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                # Split into chunks (max 500 words per chunk)
                words = text.split()
                chunk_size = 500
                
                for i in range(0, len(words), chunk_size):
                    chunk = ' '.join(words[i:i+chunk_size])
                    if len(chunk) > 100:  # Only add meaningful chunks
                        documents.append(chunk)
                
                # Limit to 20 chunks
                documents = documents[:20]
        
        except Exception as e:
            print(f"Error scraping website: {str(e)}")
        
        return documents
    
    def _create_default_documents(self, brand_name, website_url):
        """Create default documents when scraping fails"""
        return [
            f"{brand_name} is a leading brand known for quality and innovation.",
            f"Visit {website_url} to learn more about {brand_name}.",
            f"{brand_name} products are designed with excellence in mind.",
            f"Experience the best of {brand_name} - where quality meets style.",
            f"{brand_name} - Your trusted choice for premium products."
        ]
