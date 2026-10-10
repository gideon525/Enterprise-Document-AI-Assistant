# Reasoner Agent: synthesizes retrieved evidence into a grounded draft answer.

from src.llm.gemini_client import generate_with_retry


def reason_over_evidence(question, evidence):
    """Generate a draft answer using only the retrieved evidence."""
    if not evidence:
        return "The retrieved documents do not contain enough evidence to answer the question."

    # Format retrieved chunks with source information for traceability.
    evidence_text = "\n\n".join(
        [
            (
                f"Source: {item['source']}\n"
                f"Chunk: {item['chunk_index']}\n"
                f"Content:\n{item['content']}"
            )
            for item in evidence
        ]
    )

    prompt = f"""
You are the Reasoner Agent in an enterprise document question-answering system.

Answer the user's question using only the retrieved evidence provided below.

Rules:
- Do not use outside knowledge.
- Do not invent unsupported information.
- Synthesize information across relevant evidence when appropriate.
- If the evidence is insufficient, clearly say so.
- Produce a concise but complete draft answer.

USER QUESTION:
{question}

RETRIEVED EVIDENCE:
{evidence_text}
"""

    return generate_with_retry(prompt)