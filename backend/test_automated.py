#!/usr/bin/env python3
"""
Automated Testing Suite for Brand Caption Generation System
Run this to generate metrics for your research paper
"""

import os
import sys
import json
import time
from datetime import datetime
import requests
from PIL import Image

# Configuration
API_URL = "http://localhost:5000"
RESULTS_DIR = "test_results"

# Create results directory
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(f"{RESULTS_DIR}/logs", exist_ok=True)

print("=" * 80)
print("BRAND CAPTION GENERATION - AUTOMATED TESTING SUITE")
print("=" * 80)
print()

class TestSuite:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {}
        }
    
    def log(self, message, level="INFO"):
        """Log messages to console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        print(log_msg)
        
        with open(f"{RESULTS_DIR}/logs/test_run.log", "a") as f:
            f.write(log_msg + "\n")
    
    def test_api_health(self):
        """Test 1: API Health Check"""
        self.log("=" * 80)
        self.log("TEST 1: API Health Check")
        self.log("=" * 80)
        
        try:
            response = requests.get(f"{API_URL}/api/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ API is healthy", "SUCCESS")
                return True
            else:
                self.log(f"❌ API returned status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ API connection failed: {str(e)}", "ERROR")
            return False
    
    def test_brand_addition(self, brands):
        """Test 2: Brand Addition Performance"""
        self.log("\n" + "=" * 80)
        self.log("TEST 2: Brand Addition Performance")
        self.log("=" * 80)
        
        results = []
        
        for brand_name, website in brands.items():
            self.log(f"\nAdding brand: {brand_name} ({website})")
            
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{API_URL}/api/brands/add",
                    json={
                        "brand_name": brand_name,
                        "website_url": website
                    },
                    timeout=120
                )
                
                elapsed_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    docs_added = data.get('documents_added', 0)
                    
                    self.log(f"✅ Brand added successfully", "SUCCESS")
                    self.log(f"   Time taken: {elapsed_time:.2f}s")
                    self.log(f"   Documents: {docs_added}")
                    
                    results.append({
                        "brand": brand_name,
                        "success": True,
                        "time": elapsed_time,
                        "documents": docs_added
                    })
                else:
                    self.log(f"❌ Failed: {response.text}", "ERROR")
                    results.append({
                        "brand": brand_name,
                        "success": False,
                        "time": elapsed_time,
                        "error": response.text
                    })
            
            except Exception as e:
                elapsed_time = time.time() - start_time
                self.log(f"❌ Exception: {str(e)}", "ERROR")
                results.append({
                    "brand": brand_name,
                    "success": False,
                    "time": elapsed_time,
                    "error": str(e)
                })
        
        # Summary
        successful = sum(1 for r in results if r['success'])
        avg_time = sum(r['time'] for r in results) / len(results)
        
        self.log(f"\n📊 Brand Addition Summary:")
        self.log(f"   Success Rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
        self.log(f"   Average Time: {avg_time:.2f}s")
        
        return results
    
    def test_caption_generation(self, test_images, brands):
        """Test 3: Caption Generation Performance"""
        self.log("\n" + "=" * 80)
        self.log("TEST 3: Caption Generation Performance")
        self.log("=" * 80)
        
        results = []
        
        for image_path, image_name in test_images:
            if not os.path.exists(image_path):
                self.log(f"⚠️  Image not found: {image_path}", "WARNING")
                continue
            
            self.log(f"\n📸 Testing image: {image_name}")
            
            for brand_name in brands.keys():
                self.log(f"   Brand: {brand_name}")
                
                start_time = time.time()
                
                try:
                    with open(image_path, 'rb') as img_file:
                        files = {'image': img_file}
                        data = {
                            'brand_name': brand_name,
                            'personality': 'excitement'
                        }
                        
                        response = requests.post(
                            f"{API_URL}/api/caption/generate",
                            files=files,
                            data=data,
                            timeout=60
                        )
                    
                    elapsed_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        caption = result.get('final_caption', '')
                        base_caption = result.get('base_caption', '')
                        hashtags = result.get('hashtags', [])
                        
                        self.log(f"   ✅ Generated in {elapsed_time:.2f}s")
                        self.log(f"      Base: {base_caption[:60]}...")
                        self.log(f"      Final: {caption[:60]}...")
                        self.log(f"      Tags: {', '.join(hashtags[:3])}")
                        
                        results.append({
                            "image": image_name,
                            "brand": brand_name,
                            "success": True,
                            "time": elapsed_time,
                            "base_caption": base_caption,
                            "final_caption": caption,
                            "hashtags": hashtags,
                            "caption_length": len(caption)
                        })
                    else:
                        self.log(f"   ❌ Failed: {response.text[:100]}", "ERROR")
                        results.append({
                            "image": image_name,
                            "brand": brand_name,
                            "success": False,
                            "time": elapsed_time,
                            "error": response.text
                        })
                
                except Exception as e:
                    elapsed_time = time.time() - start_time
                    self.log(f"   ❌ Exception: {str(e)}", "ERROR")
                    results.append({
                        "image": image_name,
                        "brand": brand_name,
                        "success": False,
                        "time": elapsed_time,
                        "error": str(e)
                    })
        
        # Summary
        successful = sum(1 for r in results if r['success'])
        if successful > 0:
            avg_time = sum(r['time'] for r in results if r['success']) / successful
            avg_caption_length = sum(r.get('caption_length', 0) for r in results if r['success']) / successful
            
            self.log(f"\n📊 Caption Generation Summary:")
            self.log(f"   Success Rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
            self.log(f"   Average Time: {avg_time:.2f}s")
            self.log(f"   Avg Caption Length: {avg_caption_length:.0f} chars")
        
        return results
    
    def test_personality_variants(self, image_path, brand_name):
        """Test 4: Personality Variation"""
        self.log("\n" + "=" * 80)
        self.log("TEST 4: Personality Variation Test")
        self.log("=" * 80)
        
        personalities = ['sincerity', 'excitement', 'competence', 'sophistication', 'ruggedness']
        results = []
        
        self.log(f"\nTesting personalities for {brand_name}")
        
        for personality in personalities:
            self.log(f"\n   Personality: {personality.upper()}")
            
            try:
                with open(image_path, 'rb') as img_file:
                    files = {'image': img_file}
                    data = {
                        'brand_name': brand_name,
                        'personality': personality
                    }
                    
                    response = requests.post(
                        f"{API_URL}/api/caption/generate",
                        files=files,
                        data=data,
                        timeout=60
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    caption = result.get('final_caption', '')
                    
                    self.log(f"      Caption: {caption}")
                    
                    results.append({
                        "personality": personality,
                        "caption": caption,
                        "success": True
                    })
                else:
                    self.log(f"      ❌ Failed", "ERROR")
                    results.append({
                        "personality": personality,
                        "success": False,
                        "error": response.text
                    })
            
            except Exception as e:
                self.log(f"      ❌ Exception: {str(e)}", "ERROR")
                results.append({
                    "personality": personality,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def save_results(self, brand_results, caption_results, personality_results):
        """Save all results to JSON file"""
        self.log("\n" + "=" * 80)
        self.log("Saving Results")
        self.log("=" * 80)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "brand_addition": brand_results,
            "caption_generation": caption_results,
            "personality_variation": personality_results,
            "summary": {
                "total_brands": len(brand_results),
                "successful_brands": sum(1 for r in brand_results if r['success']),
                "total_captions": len(caption_results),
                "successful_captions": sum(1 for r in caption_results if r['success']),
                "avg_brand_time": sum(r['time'] for r in brand_results) / len(brand_results) if brand_results else 0,
                "avg_caption_time": sum(r['time'] for r in caption_results if r['success']) / sum(1 for r in caption_results if r['success']) if caption_results else 0
            }
        }
        
        # Save to JSON
        filename = f"{RESULTS_DIR}/test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.log(f"✅ Results saved to: {filename}")
        
        # Save human-readable summary
        summary_file = f"{RESULTS_DIR}/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(summary_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("BRAND CAPTION GENERATION - TEST RESULTS SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("BRAND ADDITION PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Brands: {results['summary']['total_brands']}\n")
            f.write(f"Successful: {results['summary']['successful_brands']}\n")
            f.write(f"Average Time: {results['summary']['avg_brand_time']:.2f}s\n\n")
            
            f.write("CAPTION GENERATION PERFORMANCE\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Captions: {results['summary']['total_captions']}\n")
            f.write(f"Successful: {results['summary']['successful_captions']}\n")
            f.write(f"Average Time: {results['summary']['avg_caption_time']:.2f}s\n\n")
            
            f.write("SAMPLE CAPTIONS\n")
            f.write("-" * 80 + "\n")
            for result in caption_results[:5]:
                if result['success']:
                    f.write(f"\nImage: {result['image']}\n")
                    f.write(f"Brand: {result['brand']}\n")
                    f.write(f"Caption: {result['final_caption']}\n")
                    f.write(f"Hashtags: {', '.join(result['hashtags'])}\n")
        
        self.log(f"✅ Summary saved to: {summary_file}")
        
        return results

def main():
    """Main test execution"""
    
    # Test configuration
    TEST_BRANDS = {
        "Nike": "https://www.nike.com",
        "Adidas": "https://www.adidas.com",
        "Puma": "https://www.puma.com"
    }
    
    # Test images (add your own image paths)
    TEST_IMAGES = [
        ("test_images/shoe1.jpg", "Running Shoe"),
        ("test_images/shoe2.jpg", "Basketball Shoe"),
        ("test_images/apparel1.jpg", "Sports Wear")
    ]
    
    # Initialize test suite
    suite = TestSuite()
    
    # Run tests
    suite.log("Starting automated test suite...")
    suite.log(f"API URL: {API_URL}")
    suite.log(f"Results Directory: {RESULTS_DIR}\n")
    
    # Test 1: API Health
    if not suite.test_api_health():
        suite.log("❌ API is not responding. Please start the backend first.", "ERROR")
        suite.log("Run: cd backend && python app.py")
        return
    
    # Test 2: Brand Addition
    brand_results = suite.test_brand_addition(TEST_BRANDS)
    
    # Test 3: Caption Generation
    caption_results = suite.test_caption_generation(TEST_IMAGES, TEST_BRANDS)
    
    # Test 4: Personality Variation (using first available image and brand)
    personality_results = []
    if TEST_IMAGES and brand_results:
        first_image = TEST_IMAGES[0][0]
        first_brand = list(TEST_BRANDS.keys())[0]
        if os.path.exists(first_image):
            personality_results = suite.test_personality_variants(first_image, first_brand)
    
    # Save results
    final_results = suite.save_results(brand_results, caption_results, personality_results)
    
    # Print final summary
    suite.log("\n" + "=" * 80)
    suite.log("TEST SUITE COMPLETED")
    suite.log("=" * 80)
    suite.log(f"\n📊 Final Summary:")
    suite.log(f"   Brands Added: {final_results['summary']['successful_brands']}/{final_results['summary']['total_brands']}")
    suite.log(f"   Captions Generated: {final_results['summary']['successful_captions']}/{final_results['summary']['total_captions']}")
    suite.log(f"   Avg Brand Time: {final_results['summary']['avg_brand_time']:.2f}s")
    suite.log(f"   Avg Caption Time: {final_results['summary']['avg_caption_time']:.2f}s")
    suite.log(f"\n✅ Check {RESULTS_DIR}/ for detailed results")

if __name__ == "__main__":
    main()
