# Retriever Agent: searches the vector database for relevant document evidence.

from src.vectorstore.vector_store import search_chunks


def retrieve_evidence(question, retrieval_plan, n_results=5):
    """Retrieve document chunks relevant to the question and retrieval plan."""
    if not question or not question.strip():
        return []

    # Combine the original question with the planner's retrieval guidance.
    search_query = f"""
User question:
{question}

Retrieval plan:
{retrieval_plan}
"""

    # Perform semantic search against the ChromaDB knowledge base.
    results = search_chunks(search_query, n_results=n_results)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # Package retrieved evidence with source information and similarity distance.
    evidence = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        evidence.append(
    {
        "content": document,
        "source": metadata.get("source", "Unknown"),
        "chunk_index": metadata.get("chunk_index"),
        "citation_id": (
            f"{metadata.get('source', 'Unknown')}"
            f"#chunk-{metadata.get('chunk_index')}"
        ),
        "distance": distance,
    }
)

    return evidence