# RAG pipeline for retrieving relevant document context and generating grounded answers.

import os

from dotenv import load_dotenv
from google import genai

from src.vectorstore.vector_store import search_chunks


# Load environment variables, including the Gemini API key.
load_dotenv()

# Initialize the Gemini client using the API key stored in .env.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question, n_results=3):
    """Generate a grounded answer using retrieved document context."""
    if not question or not question.strip():
        return "Please enter a question."

    # Retrieve the most relevant document chunks from ChromaDB.
    results = search_chunks(question, n_results=n_results)
    documents = results.get("documents", [[]])[0]

    if not documents:
        return "I could not find relevant information in the uploaded documents."

    # Combine retrieved chunks into context for the LLM.
    context = "\n\n---\n\n".join(documents)

    prompt = f"""
Answer the user's question using only the document context provided below.

If the context does not contain enough information to answer the question,
say that the answer could not be found in the uploaded documents.
Do not invent or assume information that is not supported by the context.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    # Generate an answer grounded in the retrieved document context.
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text