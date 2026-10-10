# Test the orchestrator's automatic answer-revision workflow.

import unittest
from unittest.mock import patch

from src.agents.agent_orchestrator import run_agentic_rag


class TestAgentOrchestrator(unittest.TestCase):

    @patch("src.agents.agent_orchestrator.validate_answer")
    @patch("src.agents.agent_orchestrator.reason_over_evidence")
    @patch("src.agents.agent_orchestrator.retrieve_evidence")
    @patch("src.agents.agent_orchestrator.create_retrieval_plan")
    def test_revises_invalid_answer(
        self, mock_planner, mock_retriever, mock_reasoner, mock_validator
    ):
        """Verify that a rejected answer is revised and validated again."""

        mock_planner.return_value = "Find relevant project experience."

        mock_retriever.return_value = [
            {
                "content": "The candidate developed machine learning models.",
                "source": "sample_document.txt",
                "chunk_index": 0,
                "distance": 0.2,
            }
        ]

        # First answer is unsupported; the second is corrected.
        mock_reasoner.side_effect = [
            "The candidate developed 100 machine learning models.",
            "The candidate developed machine learning models.",
        ]

        # First validation fails; second validation succeeds.
        mock_validator.side_effect = [
            {"is_valid": False, "feedback": "Unsupported model count."},
            {"is_valid": True, "feedback": "STATUS: VALID"},
        ]

        result = run_agentic_rag(
            "What machine learning experience does the candidate have?"
        )

        self.assertTrue(result["is_valid"])
        self.assertTrue(result["revision_performed"])
        self.assertEqual(mock_reasoner.call_count, 2)
        self.assertEqual(mock_validator.call_count, 2)
        self.assertIn("sample_document.txt", result["sources"])
        self.assertEqual(
            result["answer"],
            "The candidate developed machine learning models.",
        )


if __name__ == "__main__":
    unittest.main()