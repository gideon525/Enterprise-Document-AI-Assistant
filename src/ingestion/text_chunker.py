# Utilities for splitting extracted document text into RAG-ready chunks.

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Split document text into overlapping chunks for retrieval."""
    if not text or not text.strip():
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks