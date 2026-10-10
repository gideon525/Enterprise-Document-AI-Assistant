import streamlit as st
from pathlib import Path

from src.ingestion.document_loader import load_document
from src.ingestion.text_chunker import chunk_text
from src.vectorstore.vector_store import add_chunks
from src.agents.agent_orchestrator import run_agentic_rag


st.set_page_config(
    page_title="Enterprise Document AI",
    page_icon="📄",
    layout="wide",
)

st.title("🤖 Enterprise Document AI Assistant")
st.write(
    "Upload enterprise documents and ask questions using "
    "Retrieval-Augmented Generation and autonomous AI agents."
)


# Document upload section
st.subheader("📁 Upload Documents")

uploaded_files = st.file_uploader(
    "Choose files",
    type=["pdf", "txt", "csv", "xlsx"],
    accept_multiple_files=True,
)


# Save, process, and index uploaded documents.
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = Path("data/uploads") / uploaded_file.name

        # Save the uploaded file locally.
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Extract and prepare document content for retrieval.
        document_text = load_document(file_path)
        chunks = chunk_text(document_text)
        stored_chunks = add_chunks(chunks, uploaded_file.name)

        st.success(f"Processed and indexed: {uploaded_file.name}")
        st.write(f"Extracted characters: {len(document_text):,}")
        st.write(f"Chunks indexed: {stored_chunks}")


# Agentic question-answering section
st.subheader("💬 Ask Your Documents")

question = st.text_input(
    "Ask a question about the uploaded documents",
    placeholder="e.g., What AI and machine learning experience does Gideon have?",
)

if st.button("Ask"):
    if question.strip():
        try:
            with st.spinner(
                "Planning, retrieving evidence, reasoning, and validating..."
            ):
                result = run_agentic_rag(question)

            st.subheader("Answer")
            st.write(result["answer"])

            # Show validation status.
            if result["is_valid"]:
                st.success("Answer validated against retrieved evidence.")
            else:
                st.warning(
                    "The answer could not be fully validated against "
                    "the retrieved evidence."
                )

            # Show source documents used to generate the answer.
            if result.get("sources"):
                st.subheader("Sources")

                for source in result["sources"]:
                    st.write(f"- {source}")

            # Show whether the agents performed a corrective revision.
            if result.get("revision_performed"):
                st.info(
                    "The initial answer failed validation and was "
                    "automatically revised before being returned."
                )

        except RuntimeError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "The AI service is temporarily unavailable. "
                "Please try again later."
            )

    else:
        st.warning("Please enter a question.")