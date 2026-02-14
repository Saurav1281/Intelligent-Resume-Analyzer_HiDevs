import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    print("Testing imports...")
    from src.parser import ResumeParser
    from src.vector_store import VectorStoreManager
    from src.rag_engine import RAGEngine
    import streamlit
    # Check FAISS
    import faiss
    print("Imports successful!")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Import failed: {e}")
    sys.exit(1)

print("Setup verification complete.")
