import re

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing extra whitespaces, newlines, and special characters.
    """
    if not text:
        return ""
    
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove non-ascii characters (optional, depending on requirements)
    # text = text.encode("ascii", "ignore").decode()
    
    return text
