import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from src.utils import clean_text

class ResumeParser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> str:
        """
        Parses a resume file and returns the extracted text.
        Supported formats: .pdf, .docx, .txt
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()
        text = ""

        try:
            if file_ext == '.pdf':
                # Try PyPDFLoader first, generic and fast
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                text = " ".join([page.page_content for page in pages])
            elif file_ext == '.docx':
                loader = Docx2txtLoader(file_path)
                pages = loader.load()
                text = " ".join([page.page_content for page in pages])
            elif file_ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
                pages = loader.load()
                text = " ".join([page.page_content for page in pages])
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
             # Fallback or detailed error handling could go here
             raise RuntimeError(f"Error parsing file {file_path}: {str(e)}")

        return clean_text(text)
