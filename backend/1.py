import os
from google import genai
from google.genai import types

# 1. Initialize the client
# It will automatically look for an environment variable named 'GOOGLE_API_KEY'
# or you can pass it explicitly: client = genai.Client(api_key="YOUR_KEY")
client = genai.Client(api_key="AIzaSyC229NORKt3ajAHsSyJtloVW-exGwCtxNw")

MODEL_ID = "gemini-3-flash-preview"

def generate_brand_caption(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                # Gemini 3 introduces thinking levels. 
                # 'low' is great for fast captions.
                thinking_config=types.ThinkingConfig(thinking_level="low"),
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    brand_prompt = "Write a catchy Instagram caption for a new sustainable coffee brand."
    print(f"Using model: {MODEL_ID}\n")
    print(generate_brand_caption(brand_prompt))