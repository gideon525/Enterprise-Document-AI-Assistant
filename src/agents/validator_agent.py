# Validator Agent: checks whether a draft answer is supported by retrieved evidence.

from src.llm.gemini_client import generate_with_retry


def validate_answer(question, draft_answer, evidence):
    """Validate whether the draft answer is grounded in retrieved evidence."""
    if not evidence:
        return {
            "is_valid": False,
            "feedback": "No supporting evidence was retrieved.",
        }

    # Format retrieved evidence for validation.
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
You are the Validator Agent in an enterprise document question-answering system.

Check whether the draft answer is fully supported by the retrieved evidence.

Validation rules:
- Every factual claim should be supported by the evidence.
- Flag unsupported, exaggerated, or invented claims.
- Do not introduce new information.
- If the draft is adequately grounded, mark it VALID.
- If it contains unsupported claims, mark it INVALID and explain what should be corrected.

Return your response using exactly this format:

STATUS: VALID or INVALID
FEEDBACK: <brief explanation>

USER QUESTION:
{question}

DRAFT ANSWER:
{draft_answer}

RETRIEVED EVIDENCE:
{evidence_text}
"""

    validation_text = generate_with_retry(prompt).strip()

    # Convert the validator response into a simple structured result.
    is_valid = "STATUS: VALID" in validation_text.upper()

    return {
        "is_valid": is_valid,
        "feedback": validation_text,
    }