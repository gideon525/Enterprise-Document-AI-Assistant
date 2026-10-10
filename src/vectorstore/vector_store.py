# Vector embedding and storage utilities for semantic document retrieval.

import chromadb
from sentence_transformers import SentenceTransformer


# Local embedding model used to convert text into numerical vectors.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
# Load the local embedding model once when this module is imported.
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Persist vector data locally so embeddings survive application restarts.
chroma_client = chromadb.PersistentClient(path="data/chroma_db")

# Collection used to store and retrieve enterprise document chunks.
collection = chroma_client.get_or_create_collection(
    name="enterprise_documents"
)
def add_chunks(chunks, source_name):
    """Embed document chunks and store them in ChromaDB."""
    if not chunks:
        return 0

    # Convert each text chunk into a numerical embedding.
    embeddings = embedding_model.encode(chunks).tolist()

    # Create unique IDs and metadata for traceability.
    ids = [f"{source_name}_{index}" for index in range(len(chunks))]
    metadata = [
        {"source": source_name, "chunk_index": index}
        for index in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
    )

    return len(chunks)

def search_chunks(query, n_results=3):
    """Retrieve document chunks that are semantically similar to a query."""
    if not query or not query.strip():
        return []

    # Convert the user's question into the same embedding space as the documents.
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    return results