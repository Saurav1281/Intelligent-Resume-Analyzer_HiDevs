# Intelligent Resume Analyzer

A powerful AI-driven tool to analyze resumes against job descriptions using RAG (Retrieval Augmented Generation) and Groq LLaMA 3.

##  Getting Started

### Prerequisites

- Python 3.8+
- Groq API Key (Get one at [console.groq.com](https://console.groq.com))

### Installation

1.  Clone the repository (if applicable) or navigate to the project directory:
    ```bash
    cd intelligent_resume_analyzer
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up environment variables:
    -   Rename `.env.example` to `.env` and add your `GROQ_API_KEY`.
    -   OR enter the key in the sidebar when running the app.

### Running the App

To start the dashboard, run:

```bash
streamlit run app.py
```

##  Features

-   **Multi-Format Parsing**: Supports PDF, DOCX, and TXT resumes.
-   **Intelligent Matching**: Uses `sentence-transformers` for embeddings and LLaMA 3 for semantic understanding.
-   **Scoring & Feedback**: Provides a 0-100 match score with detailed pros/cons.
-   **Interactive UI**: Built with Streamlit for a smooth user experience.

## Project Structure

-   `src/parser.py`: Handles file parsing.
-   `src/vector_store.py`: Manages ChromaDB and embeddings.
-   `app.py`: The main frontend application.

##  Easy Run (Windows)

Just double-click the **`run.bat`** file in the project folder!

## Demo Video

https://drive.google.com/file/d/1fm1jDtyp46xP_K1W3Gr9TBi5i_VqJweO/view?usp=sharing
