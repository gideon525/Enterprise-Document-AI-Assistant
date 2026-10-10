# Utilities for loading and extracting text from supported document types.
from pypdf import PdfReader
import pandas as pd
from pathlib import Path

def load_pdf(file_path):
    """Extract text from a PDF document."""
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def load_txt(file_path):
    """Read and return text from a TXT document."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def load_csv(file_path):
    """Load a CSV file and convert its contents to text."""
    dataframe = pd.read_csv(file_path)
    return dataframe.to_string(index=False)
        
def load_excel(file_path):
    """Load an Excel file and convert its contents to text."""
    dataframe = pd.read_excel(file_path)
    return dataframe.to_string(index=False)

def load_document(file_path):
    """Load a supported document based on its file extension."""
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)
    elif extension == ".txt":
        return load_txt(file_path)
    elif extension == ".csv":
        return load_csv(file_path)
    elif extension == ".xlsx":
        return load_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")