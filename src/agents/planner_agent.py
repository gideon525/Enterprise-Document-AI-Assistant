# Planner Agent: analyzes a user's question and creates a retrieval plan.

from src.llm.gemini_client import generate_with_retry


def create_retrieval_plan(question):
    """Analyze the user's question and create a concise retrieval plan."""
    if not question or not question.strip():
        return "No valid question was provided."

    prompt = f"""
You are the Planner Agent in an enterprise document question-answering system.

Analyze the user's question and create a short retrieval plan that will help
another agent find the most relevant information in the document knowledge base.

Your plan should:
1. Identify the main information the user is asking for.
2. Identify important concepts or keywords to retrieve.
3. State what evidence should be found in the documents.
4. Do not answer the user's question yourself.

USER QUESTION:
{question}
"""

    return generate_with_retry(prompt)