#!/usr/bin/env python3
"""
Nike Brand Caption Testing - 10 Images
Tests nike11.png through nike20.png with Nike brand only
"""

import os
import sys
import json
import time
from datetime import datetime
import requests

# Configuration
API_URL = "http://localhost:5000"
RESULTS_DIR = "test_results"

os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 80)
print("NIKE BRAND CAPTION TESTING - 10 IMAGES")
print("=" * 80)
print()

# Nike images to test
NIKE_IMAGES = [
    "nike11.png", "nike12.png", "nike13.jpeg", "nike14.png", "nike15.png",
    "nike16.png", "nike17.jpg", "nike18.png", "nike19.png", "nike20.png"
]

def test_caption_generation():
    """Generate captions for all Nike images"""
    
    print("Testing Nike brand with 10 images...")
    print()
    
    results = []
    
    for idx, image_name in enumerate(NIKE_IMAGES, 1):
        image_path = f"test_images/{image_name}"
        
        if not os.path.exists(image_path):
            print(f"⚠️  Image not found: {image_path}")
            continue
        
        print(f"[{idx}/10] Processing {image_name}...")
        
        start_time = time.time()
        
        try:
            with open(image_path, 'rb') as img_file:
                files = {'image': img_file}
                data = {
                    'brand_name': 'Nike',
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
                
                print(f"    ✅ Generated in {elapsed_time:.2f}s")
                print(f"    Caption: {caption[:80]}...")
                print()
                
                results.append({
                    "image": image_name,
                    "brand": "Nike",
                    "success": True,
                    "time": elapsed_time,
                    "base_caption": base_caption,
                    "final_caption": caption,
                    "hashtags": hashtags
                })
            else:
                print(f"    ❌ Failed: {response.status_code}")
                print()
                results.append({
                    "image": image_name,
                    "brand": "Nike",
                    "success": False,
                    "time": elapsed_time,
                    "error": response.text
                })
        
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"    ❌ Error: {str(e)}")
            print()
            results.append({
                "image": image_name,
                "brand": "Nike",
                "success": False,
                "time": elapsed_time,
                "error": str(e)
            })
    
    return results

def save_results(results):
    """Save results to JSON file"""
    
    successful = sum(1 for r in results if r['success'])
    
    if successful > 0:
        avg_time = sum(r['time'] for r in results if r['success']) / successful
    else:
        avg_time = 0
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "brand": "Nike",
        "total_images": len(results),
        "successful": successful,
        "failed": len(results) - successful,
        "avg_time": avg_time,
        "caption_generation": results
    }
    
    # Save JSON
    filename = f"{RESULTS_DIR}/nike_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"   Total Images: {len(results)}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {len(results) - successful}")
    print(f"   Avg Time: {avg_time:.2f}s")
    print(f"\n✅ Results saved to: {filename}")
    
    return filename

def main():
    """Main execution"""
    
    # Check API
    try:
        response = requests.get(f"{API_URL}/api/brands", timeout=5)
        if response.status_code != 200:
            print("❌ API not responding. Start backend first:")
            print("   cd backend && python app.py")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Start backend: cd backend && python app.py")
        return
    
    # Run tests
    results = test_caption_generation()
    
    # Save results
    results_file = save_results(results)
    
    print(f"\n🎯 Next step: Calculate CLIPScore")
    print(f"   python test_clipscore.py {results_file}")

if __name__ == "__main__":
    main()