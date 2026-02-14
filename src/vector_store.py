import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class VectorStoreManager:
    def __init__(self, persist_directory="./data/faiss_index"):
        self.persist_directory = persist_directory
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Load existing index if available
        if os.path.exists(os.path.join(self.persist_directory, "index.faiss")):
            self.vector_db = FAISS.load_local(self.persist_directory, self.embedding_model, allow_dangerous_deserialization=True)
        else:
            self.vector_db = None # Lazy initialization or handle in add_resume

    def add_resume(self, text: str, metadata: dict):
        """
        Splits text and adds it to the vector store.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk, metadata=metadata) for chunk in chunks]
        
        if self.vector_db is None:
            self.vector_db = FAISS.from_documents(documents, self.embedding_model)
        else:
            self.vector_db.add_documents(documents)
            
        self.vector_db.save_local(self.persist_directory)

    def add_resume(self, text: str, metadata: dict):
        """
        Splits text and adds it to the vector store.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk, metadata=metadata) for chunk in chunks]
        self.vector_db.add_documents(documents)
        # self.vector_db.persist() # Chroma 0.4+ persists automatically or needs explicit call depending on version, generic langchain wrapper handles it usually.

    def similarity_search(self, query: str, k: int = 3):
        return self.vector_db.similarity_search(query, k=k)

    def get_retriever(self):
        return self.vector_db.as_retriever()
