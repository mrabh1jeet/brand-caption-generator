#!/usr/bin/env python3
"""
Human Evaluation Survey Generator
Creates evaluation forms for human raters to assess caption quality
"""

import json
import os
from datetime import datetime

def generate_survey_html(results_file):
    """Generate HTML survey for human evaluation"""
    
    # Load results
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    caption_results = results.get('caption_generation', [])[:30]  # Take first 30
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Brand Caption Evaluation Survey</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .caption-card {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .image-preview {{
            max-width: 400px;
            max-height: 300px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .caption-text {{
            background: #f8f9ff;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
            font-size: 16px;
        }}
        .rating-scale {{
            display: flex;
            gap: 10px;
            margin: 10px 0;
        }}
        .rating-scale label {{
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 8px 15px;
            border: 2px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .rating-scale label:hover {{
            border-color: #667eea;
            background: #f8f9ff;
        }}
        .rating-scale input[type="radio"]:checked + span {{
            font-weight: bold;
            color: #667eea;
        }}
        .question {{
            margin: 20px 0;
            padding: 15px;
            background: #fafafa;
            border-radius: 5px;
        }}
        .question h4 {{
            margin-top: 0;
            color: #333;
        }}
        textarea {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-family: Arial, sans-serif;
            resize: vertical;
        }}
        .submit-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 30px;
        }}
        .submit-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        .brand-label {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 Brand Caption Evaluation Survey</h1>
        <p>Help us evaluate the quality of AI-generated social media captions</p>
        <p><strong>Instructions:</strong> Rate each caption on three criteria using a 1-5 scale</p>
    </div>

    <form id="evaluationForm">
        <input type="hidden" name="evaluator_id" id="evaluatorId">
"""

    for idx, result in enumerate(caption_results, 1):
        if not result.get('success'):
            continue
        
        image_name = result['image']
        brand = result['brand']
        caption = result['final_caption']
        hashtags = ', '.join(result.get('hashtags', []))
        
        html_content += f"""
        <div class="caption-card">
            <h3>Caption {idx}</h3>
            <span class="brand-label">{brand}</span>
            
            <div class="caption-text">
                <strong>Caption:</strong> {caption}
            </div>
            
            {f'<p><strong>Hashtags:</strong> {hashtags}</p>' if hashtags else ''}
            
            <div class="question">
                <h4>1. Brand Alignment (Does the caption match {brand}'s brand voice?)</h4>
                <div class="rating-scale">
                    <label>
                        <input type="radio" name="brand_align_{idx}" value="1" required>
                        <span>1 - Poor</span>
                    </label>
                    <label>
                        <input type="radio" name="brand_align_{idx}" value="2">
                        <span>2 - Fair</span>
                    </label>
                    <label>
                        <input type="radio" name="brand_align_{idx}" value="3">
                        <span>3 - Good</span>
                    </label>
                    <label>
                        <input type="radio" name="brand_align_{idx}" value="4">
                        <span>4 - Very Good</span>
                    </label>
                    <label>
                        <input type="radio" name="brand_align_{idx}" value="5">
                        <span>5 - Excellent</span>
                    </label>
                </div>
            </div>
            
            <div class="question">
                <h4>2. Engagement Potential (Would you engage with this post?)</h4>
                <div class="rating-scale">
                    <label>
                        <input type="radio" name="engagement_{idx}" value="1" required>
                        <span>1 - Unlikely</span>
                    </label>
                    <label>
                        <input type="radio" name="engagement_{idx}" value="2">
                        <span>2 - Somewhat</span>
                    </label>
                    <label>
                        <input type="radio" name="engagement_{idx}" value="3">
                        <span>3 - Maybe</span>
                    </label>
                    <label>
                        <input type="radio" name="engagement_{idx}" value="4">
                        <span>4 - Likely</span>
                    </label>
                    <label>
                        <input type="radio" name="engagement_{idx}" value="5">
                        <span>5 - Very Likely</span>
                    </label>
                </div>
            </div>
            
            <div class="question">
                <h4>3. Creativity (How creative and catchy is this caption?)</h4>
                <div class="rating-scale">
                    <label>
                        <input type="radio" name="creativity_{idx}" value="1" required>
                        <span>1 - Generic</span>
                    </label>
                    <label>
                        <input type="radio" name="creativity_{idx}" value="2">
                        <span>2 - Ordinary</span>
                    </label>
                    <label>
                        <input type="radio" name="creativity_{idx}" value="3">
                        <span>3 - Decent</span>
                    </label>
                    <label>
                        <input type="radio" name="creativity_{idx}" value="4">
                        <span>4 - Creative</span>
                    </label>
                    <label>
                        <input type="radio" name="creativity_{idx}" value="5">
                        <span>5 - Very Creative</span>
                    </label>
                </div>
            </div>
            
            <div class="question">
                <h4>4. Would you use this caption? (Optional feedback)</h4>
                <label><input type="radio" name="use_{idx}" value="yes"> Yes, as is</label><br>
                <label><input type="radio" name="use_{idx}" value="minor"> Yes, with minor edits</label><br>
                <label><input type="radio" name="use_{idx}" value="major"> No, needs major changes</label><br>
                <textarea name="feedback_{idx}" placeholder="Optional: Suggest improvements..." rows="2"></textarea>
            </div>
        </div>
"""

    html_content += """
    <div class="caption-card">
        <h3>About You (Optional)</h3>
        <p><strong>Your Role:</strong></p>
        <label><input type="radio" name="role" value="marketing"> Marketing Professional</label><br>
        <label><input type="radio" name="role" value="social_media"> Social Media Manager</label><br>
        <label><input type="radio" name="role" value="student"> Student</label><br>
        <label><input type="radio" name="role" value="other"> Other</label><br><br>
        
        <p><strong>Years of Experience:</strong></p>
        <label><input type="radio" name="experience" value="0-2"> 0-2 years</label><br>
        <label><input type="radio" name="experience" value="3-5"> 3-5 years</label><br>
        <label><input type="radio" name="experience" value="5+"> 5+ years</label><br>
    </div>

    <button type="submit" class="submit-btn">Submit Evaluation</button>
</form>

<script>
    // Generate random evaluator ID
    document.getElementById('evaluatorId').value = 'EVAL_' + Math.random().toString(36).substr(2, 9);
    
    document.getElementById('evaluationForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Collect all form data
        const formData = new FormData(this);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Save to JSON
        const jsonData = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonData], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'evaluation_' + data.evaluator_id + '.json';
        a.click();
        
        alert('Thank you! Your evaluation has been downloaded. Please email the file to the researcher.');
    });
</script>
</body>
</html>
"""
    
    return html_content

def main():
    """Generate survey"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_human_eval.py <results_file.json>")
        return
    
    results_file = sys.argv[1]
    
    if not os.path.exists(results_file):
        print(f"❌ File not found: {results_file}")
        return
    
    print("Generating human evaluation survey...")
    
    html_content = generate_survey_html(results_file)
    
    output_file = results_file.replace('.json', '_survey.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Survey generated: {output_file}")
    print(f"\n📋 Next steps:")
    print(f"   1. Open {output_file} in a web browser")
    print(f"   2. Share with evaluators")
    print(f"   3. Collect downloaded JSON files")
    print(f"   4. Analyze results")

if __name__ == "__main__":
    main()
