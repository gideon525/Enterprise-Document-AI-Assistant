# Agent Orchestrator: coordinates the Planner, Retriever, Reasoner, and Validator agents.

from src.agents.planner_agent import create_retrieval_plan
from src.agents.retriever_agent import retrieve_evidence
from src.agents.reasoner_agent import reason_over_evidence
from src.agents.validator_agent import validate_answer


def run_agentic_rag(question):
    """Run the complete agentic RAG workflow for a user question."""
    if not question or not question.strip():
        return {
            "answer": "Please enter a question.",
            "is_valid": False,
            "sources": [],
        }

    # Step 1: Planner decides what information should be retrieved.
    retrieval_plan = create_retrieval_plan(question)

    # Step 2: Retriever searches the vector database for supporting evidence.
    evidence = retrieve_evidence(
        question,
        retrieval_plan,
        n_results=5,
    )

    if not evidence:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "is_valid": False,
            "sources": [],
        }

    # Step 3: Reasoner creates the initial grounded answer.
    draft_answer = reason_over_evidence(question, evidence)

    # Step 4: Validator checks whether the answer is supported by the evidence.
    validation = validate_answer(
        question,
        draft_answer,
        evidence,
    )

    revision_performed = False

    # Step 5: If validation fails, allow one controlled revision.
    if not validation["is_valid"]:
        revision_performed = True

        revision_question = f"""
Original user question:
{question}

The Validator Agent rejected the previous draft.

Validator feedback:
{validation["feedback"]}

Revise the answer to address the validator's concerns.
Remove unsupported claims and use only the retrieved evidence.
"""

        draft_answer = reason_over_evidence(
            revision_question,
            evidence,
        )

        # Validate the revised answer once more.
        validation = validate_answer(
            question,
            draft_answer,
            evidence,
        )

    # Collect unique source documents used during retrieval.
    sources = list(
        dict.fromkeys(
            item["source"] for item in evidence
        )
    )
    
        # Collect unique document-chunk citation references.
    citations = list(
        dict.fromkeys(
            item.get("citation_id", f"{item['source']}#chunk-{item.get('chunk_index')}")
            for item in evidence
        )
    )
    
    return {
        "answer": draft_answer,
        "is_valid": validation["is_valid"],
        "validation_feedback": validation["feedback"],
        "retrieval_plan": retrieval_plan,
        "sources": sources,
        "citations": citations,
        "evidence": evidence,
        "revision_performed": revision_performed,
    }