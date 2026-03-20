#!/usr/bin/env python3
"""
ChromaDB Data Viewer and Manager
Run this to see what brand data is stored in your vector database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import ChromaDB and sentence transformers
import chromadb
from sentence_transformers import SentenceTransformer

print("=" * 60)
print("CHROMADB DATA VIEWER")
print("=" * 60)
print()

# Initialize ChromaDB
persist_dir = os.getenv('CHROMA_PERSIST_DIR', './chroma_db')
print(f"📂 Database location: {persist_dir}")
print()

client = chromadb.PersistentClient(path=persist_dir)
collection = client.get_or_create_collection(
    name="brand_knowledge",
    metadata={"description": "Brand knowledge base for caption generation"}
)

# Load embedding model once at startup (with error handling)
print("Loading embedding model for search...")
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Embedding model loaded")
    search_available = True
except Exception as e:
    print(f"⚠ Could not load embedding model: {str(e)[:100]}")
    print("Search feature will be disabled.")
    embedding_model = None
    search_available = False
print()

# Get all data
all_data = collection.get()

print(f"📊 Total documents in database: {len(all_data['documents'])}")
print()

# Get unique brands
brands = set()
if all_data['metadatas']:
    for metadata in all_data['metadatas']:
        if 'brand' in metadata:
            brands.add(metadata['brand'])

print(f"🏢 Brands in database: {len(brands)}")
for brand in sorted(brands):
    # Count documents per brand
    brand_docs = [m for m in all_data['metadatas'] if m.get('brand') == brand]
    print(f"   • {brand}: {len(brand_docs)} documents")

print()
print("=" * 60)

# Interactive menu
while True:
    print()
    print("What would you like to do?")
    print("1. View all brands")
    print("2. View documents for a specific brand")
    print("3. Search for content")
    print("4. Delete a brand")
    print("5. Clear entire database")
    print("6. Export brand data to text file")
    print("0. Exit")
    print()
    
    choice = input("Enter your choice (0-6): ").strip()
    
    if choice == "0":
        print("Goodbye!")
        break
    
    elif choice == "1":
        print()
        print("=" * 60)
        print("ALL BRANDS IN DATABASE")
        print("=" * 60)
        for brand in sorted(brands):
            brand_docs = [m for m in all_data['metadatas'] if m.get('brand') == brand]
            print(f"\n📦 {brand.upper()}")
            print(f"   Documents: {len(brand_docs)}")
            
            # Show first document preview
            brand_indices = [i for i, m in enumerate(all_data['metadatas']) if m.get('brand') == brand]
            if brand_indices:
                first_doc = all_data['documents'][brand_indices[0]]
                preview = first_doc[:200] + "..." if len(first_doc) > 200 else first_doc
                print(f"   Preview: {preview}")
    
    elif choice == "2":
        brand_name_input = input("\nEnter brand name: ").strip()
        
        # Find the actual brand name (case-insensitive)
        actual_brand = None
        for brand in brands:
            if brand.lower() == brand_name_input.lower():
                actual_brand = brand
                break
        
        if not actual_brand:
            print(f"❌ Brand '{brand_name_input}' not found.")
            print(f"Available brands: {', '.join(sorted(brands))}")
            continue
        
        print()
        print("=" * 60)
        print(f"DOCUMENTS FOR {actual_brand.upper()}")
        print("=" * 60)
        
        # Get all documents for this brand
        brand_indices = [i for i, m in enumerate(all_data['metadatas']) if m.get('brand') == actual_brand]
        
        if not brand_indices:
            print(f"❌ No documents found for '{actual_brand}'")
        else:
            for idx, i in enumerate(brand_indices, 1):
                doc = all_data['documents'][i]
                print(f"\n📄 Document {idx}:")
                print(f"   Length: {len(doc)} characters")
                print(f"   Content: {doc[:500]}...")
                print()
    
    elif choice == "3":
        if not search_available:
            print("\n❌ Search is not available (embedding model failed to load)")
            print("You can still view brand documents using option 2")
            continue
        
        query = input("\nEnter search query: ").strip()
        print()
        
        # Generate query embedding
        query_embedding = embedding_model.encode([query])[0].tolist()
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        print("=" * 60)
        print(f"SEARCH RESULTS FOR: '{query}'")
        print("=" * 60)
        
        if results['documents'][0]:
            for idx, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][idx-1]
                brand = metadata.get('brand', 'Unknown')
                print(f"\n🔍 Result {idx} (Brand: {brand})")
                print(f"   {doc[:300]}...")
        else:
            print("No results found.")
    
    elif choice == "4":
        brand_name_input = input("\nEnter brand name to delete: ").strip()
        
        # Find actual brand name
        actual_brand = None
        for brand in brands:
            if brand.lower() == brand_name_input.lower():
                actual_brand = brand
                break
        
        if not actual_brand:
            print(f"❌ Brand '{brand_name_input}' not found.")
            print(f"Available brands: {', '.join(sorted(brands))}")
            continue
        
        confirm = input(f"⚠️  Are you sure you want to delete all data for '{actual_brand}'? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            # Get all IDs for the brand
            results = collection.get(where={"brand": actual_brand})
            
            if results['ids']:
                collection.delete(ids=results['ids'])
                print(f"✅ Deleted {len(results['ids'])} documents for '{actual_brand}'")
                brands.discard(actual_brand)
                all_data = collection.get()
            else:
                print(f"❌ No documents found for '{actual_brand}'")
        else:
            print("Cancelled.")
    
    elif choice == "5":
        confirm = input("⚠️  Are you ABSOLUTELY sure you want to delete ALL data? (type 'DELETE ALL'): ").strip()
        
        if confirm == "DELETE ALL":
            # Delete the collection
            client.delete_collection("brand_knowledge")
            print("✅ All data deleted!")
            print("Creating new empty collection...")
            collection = client.get_or_create_collection(
                name="brand_knowledge",
                metadata={"description": "Brand knowledge base for caption generation"}
            )
            brands = set()
            all_data = collection.get()
            print("Done.")
        else:
            print("Cancelled.")
    
    elif choice == "6":
        brand_name_input = input("\nEnter brand name to export (or 'all' for everything): ").strip()
        
        if brand_name_input.lower() == 'all':
            filename = "all_brands_export.txt"
            export_docs = all_data['documents']
            export_metas = all_data['metadatas']
        else:
            # Find actual brand name
            actual_brand = None
            for brand in brands:
                if brand.lower() == brand_name_input.lower():
                    actual_brand = brand
                    break
            
            if not actual_brand:
                print(f"❌ Brand '{brand_name_input}' not found.")
                print(f"Available brands: {', '.join(sorted(brands))}")
                continue
            
            filename = f"{actual_brand}_export.txt"
            brand_indices = [i for i, m in enumerate(all_data['metadatas']) if m.get('brand') == actual_brand]
            export_docs = [all_data['documents'][i] for i in brand_indices]
            export_metas = [all_data['metadatas'][i] for i in brand_indices]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("BRAND DATA EXPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total Documents: {len(export_docs)}\n")
            f.write(f"Export Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n\n")
            
            for idx, (doc, meta) in enumerate(zip(export_docs, export_metas), 1):
                brand = meta.get('brand', 'Unknown')
                doc_id = meta.get('doc_id', 'N/A')
                
                # Header for each document
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"DOCUMENT {idx}\n")
                f.write("=" * 80 + "\n")
                f.write(f"Brand: {brand}\n")
                f.write(f"Document ID: {doc_id}\n")
                f.write(f"Length: {len(doc)} characters\n")
                f.write("-" * 80 + "\n\n")
                
                # Format the content with proper line breaks
                # Split into sentences for better readability
                import re
                
                # Replace common separators with line breaks
                formatted_doc = doc
                
                # Add line breaks after periods followed by capital letters
                formatted_doc = re.sub(r'\.([A-Z])', r'.\n\n\1', formatted_doc)
                
                # Add line breaks after common section markers
                formatted_doc = re.sub(r'(Shop [A-Z])', r'\n\n\1', formatted_doc)
                formatted_doc = re.sub(r'(Learn more)', r'\n\n\1', formatted_doc)
                formatted_doc = re.sub(r'(New & Featured)', r'\n\n\1', formatted_doc)
                
                # Wrap long lines at 80 characters
                lines = []
                for line in formatted_doc.split('\n'):
                    if len(line) <= 80:
                        lines.append(line)
                    else:
                        # Wrap at word boundaries
                        words = line.split()
                        current_line = ""
                        for word in words:
                            if len(current_line) + len(word) + 1 <= 80:
                                current_line += word + " "
                            else:
                                lines.append(current_line.strip())
                                current_line = word + " "
                        if current_line:
                            lines.append(current_line.strip())
                
                f.write('\n'.join(lines))
                f.write("\n\n")
        
        print(f"✅ Exported {len(export_docs)} documents to '{filename}'")
        print(f"📁 File location: {os.path.abspath(filename)}")
    
    else:
        print("❌ Invalid choice. Please try again.")

print()
print("=" * 60)