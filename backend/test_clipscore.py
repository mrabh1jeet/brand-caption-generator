#!/usr/bin/env python3
"""
Nike Caption Test with CLIPScore
Tests nike11-20 with Nike brand and calculates real CLIPScore
"""

import os
import json
import time
from datetime import datetime
import requests
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# Configuration
API_URL = "http://localhost:5000"
RESULTS_DIR = "test_results"

os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 80)
print("NIKE CAPTION TEST WITH CLIPSCORE")
print("=" * 80)
print()

# Load CLIP model once
print("Loading CLIP model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model.eval()
print(f"✅ CLIP loaded on {device}\n")

def calculate_clipscore(image_path, caption):
    """Calculate REAL CLIPScore"""
    try:
        image = Image.open(image_path).convert("RGB")
        
        inputs = clip_processor(
            text=[caption],
            images=image,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(device)
        
        with torch.no_grad():
            outputs = clip_model(**inputs)
            
            # Normalize embeddings
            image_embeds = outputs.image_embeds / outputs.image_embeds.norm(dim=-1, keepdim=True)
            text_embeds = outputs.text_embeds / outputs.text_embeds.norm(dim=-1, keepdim=True)
            
            # Cosine similarity
            similarity = (image_embeds * text_embeds).sum(dim=-1).item()
        
        return float(similarity)
    
    except Exception as e:
        print(f"    ❌ CLIPScore error: {e}")
        return 0.0

def test_nike_images():
    """Test all Nike images and calculate CLIPScore"""
    
    # Check API is running
    try:
        response = requests.get(f"{API_URL}/api/brands", timeout=5)
        if response.status_code != 200:
            print("❌ API not responding!")
            print("   Start backend: cd backend && python app.py")
            return None
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Make sure backend is running on port 5000")
        return None
    
    print("✅ API is running\n")
    
    # Nike images
    nike_images = [
        "nike11.png", "nike12.png", "nike13.jpeg", "nike14.png", "nike15.png",
        "nike16.png", "nike17.jpg", "nike18.png", "nike19.png", "nike20.png"
    ]
    
    results = []
    
    for idx, image_name in enumerate(nike_images, 1):
        image_path = f"test_images/{image_name}"
        
        if not os.path.exists(image_path):
            print(f"⚠️  Skipping {image_name} - not found")
            continue
        
        print(f"[{idx}/10] {image_name}")
        
        # Generate caption via API
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
                    timeout=90
                )
            
            generation_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                base_caption = result.get('base_caption', '')
                final_caption = result.get('final_caption', '')
                hashtags = result.get('hashtags', [])
                
                # Calculate CLIPScore on THE SAME IMAGE
                base_score = calculate_clipscore(image_path, base_caption) if base_caption else 0.0
                final_score = calculate_clipscore(image_path, final_caption)
                
                print(f"    ✅ Generated in {generation_time:.1f}s")
                print(f"    Base CLIPScore:  {base_score:.3f}")
                print(f"    Final CLIPScore: {final_score:.3f}")
                print(f"    Caption: {final_caption[:70]}...")
                print()
                
                results.append({
                    "image": image_name,
                    "image_path": image_path,
                    "brand": "Nike",
                    "personality": "excitement",
                    "success": True,
                    "generation_time": generation_time,
                    "base_caption": base_caption,
                    "final_caption": final_caption,
                    "hashtags": hashtags,
                    "base_clipscore": base_score,
                    "final_clipscore": final_score,
                    "improvement": final_score - base_score
                })
            
            else:
                print(f"    ❌ API Error: {response.status_code}")
                print(f"    {response.text[:100]}")
                print()
                
                results.append({
                    "image": image_name,
                    "success": False,
                    "error": response.text
                })
        
        except Exception as e:
            print(f"    ❌ Exception: {str(e)}")
            print()
            
            results.append({
                "image": image_name,
                "success": False,
                "error": str(e)
            })
    
    return results

def save_results(results):
    """Save results with summary"""
    
    successful = [r for r in results if r.get('success', False)]
    
    if not successful:
        print("❌ No successful tests!")
        return None
    
    # Calculate statistics
    avg_gen_time = sum(r['generation_time'] for r in successful) / len(successful)
    avg_clip = sum(r['final_clipscore'] for r in successful) / len(successful)
    min_clip = min(r['final_clipscore'] for r in successful)
    max_clip = max(r['final_clipscore'] for r in successful)
    
    # Calculate std dev
    import math
    variance = sum((r['final_clipscore'] - avg_clip) ** 2 for r in successful) / len(successful)
    std_dev = math.sqrt(variance)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "brand": "Nike",
        "total_images": len(results),
        "successful": len(successful),
        "failed": len(results) - len(successful),
        "statistics": {
            "avg_generation_time": round(avg_gen_time, 2),
            "avg_clipscore": round(avg_clip, 3),
            "std_dev": round(std_dev, 3),
            "min_clipscore": round(min_clip, 3),
            "max_clipscore": round(max_clip, 3)
        },
        "results": results
    }
    
    # Interpretation
    if avg_clip >= 0.30:
        interpretation = "✅ EXCELLENT - Strong alignment"
    elif avg_clip >= 0.25:
        interpretation = "✅ GOOD - Reasonable alignment"
    elif avg_clip >= 0.20:
        interpretation = "⚠️ FAIR - Acceptable alignment"
    else:
        interpretation = "❌ POOR - Needs improvement"
    
    summary["interpretation"] = interpretation
    
    # Save
    filename = f"{RESULTS_DIR}/nike_clipscore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\nImages Tested: {len(successful)}/{len(results)}")
    print(f"Avg Generation Time: {avg_gen_time:.2f}s")
    print(f"\nCLIPScore Results:")
    print(f"  Average: {avg_clip:.3f} ± {std_dev:.3f}")
    print(f"  Range: {min_clip:.3f} to {max_clip:.3f}")
    print(f"\n{interpretation}")
    print(f"\n✅ Results saved to: {filename}")
    print()
    print("Note: CLIP similarity scores typically range 0.20-0.35 for good captions")
    print("      Scores above 0.30 indicate strong image-caption alignment")
    
    return filename

def main():
    """Run Nike caption test with CLIPScore"""
    
    results = test_nike_images()
    
    if results:
        save_results(results)
    else:
        print("❌ Test failed - check if backend is running")

if __name__ == "__main__":
    main()