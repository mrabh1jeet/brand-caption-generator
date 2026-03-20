import chromadb
from chromadb.config import Settings
import os
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(self):
        """Initialize ChromaDB and embedding model"""
        print("Initializing RAG Service...")
        
        # Initialize ChromaDB
        persist_dir = os.getenv('CHROMA_PERSIST_DIR', './chroma_db')
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="brand_knowledge",
            metadata={"description": "Brand knowledge base for caption generation"}
        )
        
        print("RAG Service initialized")
    
    def add_brand_documents(self, brand_name, documents):
        """
        Add brand documents to the knowledge base
        
        Args:
            brand_name: Name of the brand
            documents: List of text documents
        """
        try:
            if not documents:
                return
            
            # Generate IDs
            ids = [f"{brand_name}_{i}" for i in range(len(documents))]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Create metadata
            metadatas = [{"brand": brand_name, "doc_id": i} for i in range(len(documents))]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Added {len(documents)} documents for brand {brand_name}")
        
        except Exception as e:
            raise Exception(f"Error adding documents: {str(e)}")
    
    def retrieve_brand_context(self, brand_name, query, personality, top_k=5):
        """
        Retrieve relevant brand context
        
        Args:
            brand_name: Name of the brand
            query: Query text (base caption)
            personality: Brand personality
            top_k: Number of documents to retrieve
            
        Returns:
            list: Retrieved documents
        """
        try:
            # Create enhanced query
            enhanced_query = f"{query} {brand_name} {personality}"
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([enhanced_query])[0].tolist()
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={"brand": brand_name}
            )
            
            # Extract documents
            documents = results['documents'][0] if results['documents'] else []
            
            return documents
        
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def get_available_brands(self):
        """Get list of available brands in the knowledge base"""
        try:
            # Get all documents
            all_docs = self.collection.get()
            
            # Extract unique brands
            brands = set()
            if all_docs['metadatas']:
                for metadata in all_docs['metadatas']:
                    if 'brand' in metadata:
                        brands.add(metadata['brand'])
            
            return sorted(list(brands))
        
        except Exception as e:
            print(f"Error getting brands: {str(e)}")
            return []
    
    def clear_brand(self, brand_name):
        """Remove all documents for a specific brand"""
        try:
            # Get all IDs for the brand
            results = self.collection.get(where={"brand": brand_name})
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                print(f"Cleared {len(results['ids'])} documents for brand {brand_name}")
        
        except Exception as e:
            raise Exception(f"Error clearing brand: {str(e)}")
