#!/usr/bin/env python3
"""
Test script to diagnose backend issues
Run this from the backend folder with: python test_services.py
"""

import sys
import os

print("=" * 60)
print("BRAND CAPTION SYSTEM - DIAGNOSTIC TEST")
print("=" * 60)
print()

# Test 1: Check Python version
print("1. Python Version:")
print(f"   {sys.version}")
print()

# Test 2: Check imports
print("2. Testing imports...")
test_results = {}

try:
    import flask
    test_results['Flask'] = '✓ OK'
except Exception as e:
    test_results['Flask'] = f'✗ FAILED: {str(e)}'

try:
    import google.generativeai as genai
    test_results['Google Gemini'] = '✓ OK'
except Exception as e:
    test_results['Google Gemini'] = f'✗ FAILED: {str(e)}'

try:
    import chromadb
    test_results['ChromaDB'] = '✓ OK'
except Exception as e:
    test_results['ChromaDB'] = f'✗ FAILED: {str(e)}'

try:
    from transformers import BlipProcessor
    test_results['Transformers'] = '✓ OK'
except Exception as e:
    test_results['Transformers'] = f'✗ FAILED: {str(e)}'

try:
    from PIL import Image
    test_results['Pillow'] = '✓ OK'
except Exception as e:
    test_results['Pillow'] = f'✗ FAILED: {str(e)}'

try:
    from bs4 import BeautifulSoup
    test_results['BeautifulSoup'] = '✓ OK'
except Exception as e:
    test_results['BeautifulSoup'] = f'✗ FAILED: {str(e)}'

for package, status in test_results.items():
    print(f"   {package}: {status}")
print()

# Test 3: Check .env file
print("3. Checking .env configuration...")
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"   ✓ GEMINI_API_KEY found: {gemini_key[:20]}...")
else:
    print("   ✗ GEMINI_API_KEY not found in .env")
print()

# Test 4: Test Gemini API
print("4. Testing Gemini API connection...")
try:
    import google.generativeai as genai
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello, the API is working!'")
    print(f"   ✓ Gemini API Response: {response.text}")
except Exception as e:
    print(f"   ✗ Gemini API Error: {str(e)}")
print()

# Test 5: Test ChromaDB
print("5. Testing ChromaDB...")
try:
    import chromadb
    client = chromadb.Client()
    collection = client.create_collection(name="test_collection")
    print("   ✓ ChromaDB is working")
except Exception as e:
    print(f"   ✗ ChromaDB Error: {str(e)}")
print()

# Test 6: Test web scraping
print("6. Testing web scraping...")
try:
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get("https://example.com", timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"   ✓ Web scraping is working (status: {response.status_code})")
except Exception as e:
    print(f"   ✗ Web scraping Error: {str(e)}")
print()

# Test 7: Check if services can be initialized
print("7. Testing service initialization...")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services'))
    
    # Test RAG Service
    from rag_service import RAGService
    rag = RAGService()
    print("   ✓ RAG Service initialized")
except Exception as e:
    print(f"   ✗ RAG Service Error: {str(e)}")

try:
    from caption_generator import CaptionGeneratorService
    caption_gen = CaptionGeneratorService()
    print("   ✓ Caption Generator Service initialized")
except Exception as e:
    print(f"   ✗ Caption Generator Error: {str(e)}")

try:
    from brand_scraper import BrandScraperService
    scraper = BrandScraperService()
    print("   ✓ Brand Scraper Service initialized")
except Exception as e:
    print(f"   ✗ Brand Scraper Error: {str(e)}")

print()
print("=" * 60)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 60)
print()
print("If all tests passed, the backend should work correctly.")
print("If any test failed, install the missing package:")
print("  pip install <package-name>")
