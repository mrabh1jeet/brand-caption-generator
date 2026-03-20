#!/usr/bin/env python3
"""
CLIPScore Evaluation for Image-Caption Alignment
Measures how well generated captions match the actual image content
"""

import os
import json
import torch
from PIL import Image
import numpy as np

print("Installing required packages...")
print("Run: pip install transformers ftfy")
print()

try:
    from transformers import CLIPProcessor, CLIPModel
except ImportError:
    print("❌ Error: transformers not installed")
    print("Run: pip install transformers")
    exit(1)

class CLIPScoreEvaluator:
    def __init__(self):
        """Initialize CLIP model"""
        print("Loading CLIP model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        print(f"✅ CLIP model loaded on {self.device}\n")
    
    def calculate_clipscore(self, image_path, caption):
        """
        Calculate CLIPScore for an image-caption pair
        
        Args:
            image_path: Path to image
            caption: Generated caption text
            
        Returns:
            float: CLIPScore (0-1, higher is better)
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Process inputs
            inputs = self.processor(
                text=[caption],
                images=image,
                return_tensors="pt",
                padding=True
            ).to(self.device)
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Calculate similarity
            logits_per_image = outputs.logits_per_image
            score = logits_per_image.item() / 100.0  # Normalize to 0-1
            
            return score
        
        except Exception as e:
            print(f"Error calculating CLIPScore: {str(e)}")
            return 0.0
    
    def evaluate_results_file(self, results_file):
        """
        Evaluate all captions in a test results JSON file
        
        Args:
            results_file: Path to test_results.json
        """
        print("=" * 80)
        print("CLIPSCORE EVALUATION")
        print("=" * 80)
        print()
        
        # Load results
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        caption_results = results.get('caption_generation', [])
        
        if not caption_results:
            print("❌ No caption results found in file")
            return
        
        scores = []
        detailed_results = []
        
        print(f"Evaluating {len(caption_results)} captions...\n")
        
        for idx, result in enumerate(caption_results, 1):
            if not result.get('success'):
                continue
            
            image_name = result['image']
            brand = result['brand']
            caption = result['final_caption']
            base_caption = result.get('base_caption', '')
            
            # Construct image path (you may need to adjust this)
            image_path = f"test_images/{image_name}"
            
            if not os.path.exists(image_path):
                print(f"⚠️  Image not found: {image_path}")
                continue
            
            # Calculate scores
            final_score = self.calculate_clipscore(image_path, caption)
            base_score = self.calculate_clipscore(image_path, base_caption) if base_caption else 0.0
            
            improvement = final_score - base_score
            
            scores.append(final_score)
            
            detailed_results.append({
                "image": image_name,
                "brand": brand,
                "base_caption": base_caption,
                "final_caption": caption,
                "base_score": base_score,
                "final_score": final_score,
                "improvement": improvement
            })
            
            print(f"[{idx}/{len(caption_results)}] {image_name} ({brand})")
            print(f"    Base Caption Score:  {base_score:.3f}")
            print(f"    Final Caption Score: {final_score:.3f}")
            print(f"    Improvement:         {improvement:+.3f}")
            print(f"    Caption: {caption[:60]}...")
            print()
        
        # Calculate statistics
        if scores:
            avg_score = np.mean(scores)
            std_score = np.std(scores)
            min_score = np.min(scores)
            max_score = np.max(scores)
            
            print("=" * 80)
            print("SUMMARY STATISTICS")
            print("=" * 80)
            print(f"Average CLIPScore: {avg_score:.3f} ± {std_score:.3f}")
            print(f"Min Score:         {min_score:.3f}")
            print(f"Max Score:         {max_score:.3f}")
            print(f"Total Evaluated:   {len(scores)}")
            print()
            
            # Interpretation
            print("📊 INTERPRETATION:")
            if avg_score >= 0.85:
                print("✅ EXCELLENT - Captions strongly align with images")
            elif avg_score >= 0.75:
                print("✅ GOOD - Captions reasonably align with images")
            elif avg_score >= 0.65:
                print("⚠️  FAIR - Some alignment issues detected")
            else:
                print("❌ POOR - Significant alignment issues")
            print()
            
            # Save detailed results
            output_file = results_file.replace('.json', '_clipscore.json')
            with open(output_file, 'w') as f:
                json.dump({
                    "summary": {
                        "average_score": float(avg_score),
                        "std_dev": float(std_score),
                        "min_score": float(min_score),
                        "max_score": float(max_score),
                        "total_evaluated": len(scores)
                    },
                    "detailed_results": detailed_results
                }, f, indent=2)
            
            print(f"✅ Detailed results saved to: {output_file}")
            
            return {
                "avg": avg_score,
                "std": std_score,
                "min": min_score,
                "max": max_score
            }

def main():
    """Main execution"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_clipscore.py <results_file.json>")
        print("\nExample:")
        print("  python test_clipscore.py test_results/test_results_20260219_123456.json")
        return
    
    results_file = sys.argv[1]
    
    if not os.path.exists(results_file):
        print(f"❌ File not found: {results_file}")
        return
    
    evaluator = CLIPScoreEvaluator()
    evaluator.evaluate_results_file(results_file)

if __name__ == "__main__":
    main()
