# Enterprise Document AI Assistant

### Agentic Retrieval-Augmented Generation (RAG) System

**Project Type:** AI/ML Capstone Project  
**Developer:** Gideon Abunuma  
**Programming Language:** Python 3.12  
**Application Framework:** Streamlit  
**LLM:** Google Gemini

---

## 1. Project Overview

The Enterprise Document AI Assistant is an intelligent document question-answering application that combines Retrieval-Augmented Generation (RAG), semantic search, and a multi-agent AI workflow.

The application allows users to upload enterprise documents, extract and index their contents, and ask natural-language questions grounded in the uploaded information.

Unlike a conventional chatbot, the system uses four specialized AI agents to coordinate information retrieval, answer generation, and validation.

The application also provides source citations, an Agent Execution Trace, and initial prompt-injection safeguards to improve transparency and reliability.

### Supported Document Formats

- PDF (`.pdf`)
- Text (`.txt`)
- CSV (`.csv`)
- Excel (`.xlsx`)

## 2. Project Objectives

The primary objectives are to:

1. Develop an end-to-end document ingestion and preprocessing pipeline.
2. Convert document text into embeddings for semantic retrieval.
3. Store and retrieve document embeddings using ChromaDB.
4. Integrate Google Gemini for evidence-grounded answer generation.
5. Implement a four-agent workflow consisting of Planner, Retriever, Reasoner, and Validator agents.
6. Introduce answer validation and a bounded automatic revision mechanism.
7. Provide document-level and chunk-level evidence references.
8. Display agent execution details through an interactive Streamlit interface.
9. Introduce and evaluate initial prompt-injection safeguards.
10. Deliver a reproducible AI/ML application with tests and technical documentation.

## 3. Key Features

- Multi-format document upload and text extraction
- Text chunking and embedding generation
- Persistent vector storage using ChromaDB
- Semantic retrieval of relevant document chunks
- Gemini-powered natural-language question answering
- Multi-agent planning, retrieval, reasoning, and validation
- Automatic answer revision following failed validation
- Source document and chunk-level citations
- Expandable Agent Execution Trace
- Initial prompt-injection protection
- Automated unit tests and documented security evaluation

---

## 4. System Architecture

The Enterprise Document AI Assistant uses a modular architecture combining document processing, vector-based retrieval, Google Gemini, and four specialized AI agents.

### 4.1 Architecture Diagram

```text
                 USER
                   |
                   v
           STREAMLIT INTERFACE
                   |
          +--------+--------+
          |                 |
          v                 v
    DOCUMENT UPLOAD     USER QUESTION
          |                 |
          v                 v
    TEXT EXTRACTION     PLANNER AGENT
          |                 |
          v                 v
      TEXT CHUNKING     RETRIEVER AGENT
          |                 |
          v                 |
    EMBEDDING MODEL          |
          |                 |
          v                 v
       CHROMADB <------ SEMANTIC SEARCH
                            |
                            v
                      REASONER AGENT
                            |
                            v
                      VALIDATOR AGENT
                            |
                  +---------+---------+
                  |                   |
                VALID               INVALID
                  |                   |
                  |                   v
                  |             REASONER REVISES
                  |                   |
                  |                   v
                  |             REVALIDATION
                  |                   |
                  +---------+---------+
                            |
                            v
                     FINAL RESPONSE
                            |
                            v
                ANSWER + SOURCES + TRACE
```

### 4.2 AI Agent Responsibilities

**Planner Agent**

Analyzes the user's question and produces a retrieval strategy identifying relevant concepts, keywords, and expected evidence.

**Retriever Agent**

Combines the user question with the retrieval plan and searches ChromaDB for relevant document chunks. Returns retrieved text, source metadata, chunk identifiers, and similarity-distance information.

**Reasoner Agent**

Uses Google Gemini to synthesize a grounded answer from retrieved evidence. Includes instructions to treat document content as untrusted data.

**Validator Agent**

Uses Google Gemini to assess whether the generated answer is supported by retrieved evidence. Returns a validation decision and feedback.

### 4.3 Automatic Answer Revision

If the Validator Agent rejects the initial answer, the orchestrator sends the validation feedback to the Reasoner Agent for one corrective revision.

The revised answer is validated again.

The workflow permits a maximum of one automatic revision per question. An answer that remains invalid is flagged rather than repeatedly regenerated.

### 4.4 Explainability

The Streamlit dashboard displays:

- Generated answer
- Final validation status
- Source document filenames
- Retrieved document-chunk identifiers
- Planner Agent retrieval strategy
- Retriever Agent supporting evidence
- Validator Agent feedback
- Whether an automatic answer revision occurred

Chunk-level references identify retrieved evidence but do not constitute independently verified, claim-by-claim citations.

---

## 5. Technology Stack

| Technology            | Purpose                                         |
| --------------------- | ----------------------------------------------- |
| Python 3.12           | Core application development                    |
| Streamlit             | Interactive web interface                       |
| Google Gemini         | LLM-powered planning, reasoning, and validation |
| ChromaDB              | Persistent vector database                      |
| sentence-transformers | Semantic embedding generation                   |
| all-MiniLM-L6-v2      | Pretrained embedding model                      |
| PyPDF                 | PDF text extraction                             |
| Pandas                | CSV and Excel data processing                   |
| openpyxl              | Excel file support                              |
| python-dotenv         | Environment variable configuration              |
| unittest              | Automated testing                               |
| Git                   | Version control                                 |

### 5.1 Project Structure

```text
GideonAbunuma_PGD_13_AIML/
|
|-- app.py
|-- requirements.txt
|-- README.md
|-- SECURITY_EVALUATION.md
|-- .gitignore
|
|-- src/
|   |-- __init__.py
|   |
|   |-- agents/
|   |   |-- __init__.py
|   |   |-- agent_orchestrator.py
|   |   |-- planner_agent.py
|   |   |-- retriever_agent.py
|   |   |-- reasoner_agent.py
|   |   |-- validator_agent.py
|   |
|   |-- ingestion/
|   |   |-- __init__.py
|   |   |-- document_loader.py
|   |   |-- text_chunker.py
|   |
|   |-- vectorstore/
|   |   |-- __init__.py
|   |   |-- vector_store.py
|   |
|   |-- llm/
|   |   |-- __init__.py
|   |   |-- gemini_client.py
|   |
|   |-- rag/
|       |-- __init__.py
|       |-- rag_pipeline.py
|
|-- tests/
|   |-- test_agent_orchestrator.py
|   |-- test_prompt_injection.py
|
|-- data/
|   |-- uploads/
|   |-- chroma_db/
|
|-- .venv/
|-- .env
```

### 5.2 Directory Descriptions

**src/agents/**

Contains the four AI agents and the orchestrator that coordinates the complete agentic RAG workflow.

**src/ingestion/**

Handles document extraction and text chunking.

**src/vectorstore/**

Generates embeddings and manages ChromaDB document storage and semantic retrieval.

**src/llm/**

Provides the shared Gemini client, API configuration, and retry handling.

**src/rag/**

Contains the earlier RAG pipeline implementation retained for reference.

**tests/**

Contains automated tests for the answer-revision workflow and prompt security instructions.

**data/uploads/**

Stores uploaded documents during local application execution.

**data/chroma_db/**

Stores the persistent ChromaDB vector database.

### 5.3 Local Files and Security

The following are excluded from Git version control:

- `.env` — API keys and environment configuration
- `.venv/` — Local Python virtual environment
- `data/uploads/*` — Uploaded documents
- `data/chroma_db/` — Local vector database
- Python cache files

These exclusions help prevent accidental publication of local credentials, uploaded documents, and generated data.

The application is currently intended for local development and evaluation rather than production deployment.

---

## 6. Installation and Setup

### 6.1 Prerequisites

Before running the application, ensure you have:

- Python 3.12 installed
- Git installed (recommended)
- Visual Studio Code or another Python-compatible editor
- Internet access for Gemini API requests and initial embedding-model download
- A valid Google Gemini API key

### 6.2 Download the Project

Download or clone the project repository, then open its root directory in a terminal.

For example, on Windows PowerShell:

```powershell
cd "GideonAbunuma_PGD_13_AIML"
```

### 6.3 Create a Python Virtual Environment

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Verify the Python version:

```powershell
python --version
```

The project was developed using Python 3.12.

### 6.4 Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

The required packages include Streamlit, ChromaDB, sentence-transformers, Google GenAI, Pandas, PyPDF, and openpyxl.

### 6.5 Configure the Gemini API Key

Create a file named `.env` in the project root directory.

Add the following configuration:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your actual Gemini API key.

**Security:** Never commit the `.env` file or share your API key publicly. The project's `.gitignore` excludes `.env` from version control.

### 6.6 Run the Application

From the project root directory, execute:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local application address, typically:

http://localhost:8501

Open the address in a web browser.

### 6.7 Use the Application

1. Upload a PDF, TXT, CSV, or XLSX document.
2. Wait for the application to extract, chunk, embed, and index its contents.
3. Enter a question about the uploaded information.
4. Click **Ask**.
5. Review the generated answer and validation status.
6. Inspect the source documents and retrieved evidence citations.
7. Expand **Agent Execution Trace** to view agent activity.

Previously indexed documents may also be retrieved because the application uses persistent ChromaDB storage.

### 6.8 Run Automated Tests

From the project root directory, execute:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The automated tests cover:

- Agent Orchestrator answer revision and revalidation
- Presence of prompt-injection safeguards in the Reasoner Agent's instructions

These tests use mocked AI responses and do not require live Gemini API requests.

### 6.9 Stop the Application

Return to the terminal running Streamlit and press:

**Ctrl + C**

This stops the local Streamlit server.

---

## 7. Testing and Evaluation

The Enterprise Document AI Assistant was evaluated using automated unit tests, functional application tests, and a controlled prompt-injection security test.

### 7.1 Automated Unit Tests

Two automated tests were implemented using Python's built-in `unittest` framework.

| Test                          | Purpose                                                                                 | Result |
| ----------------------------- | --------------------------------------------------------------------------------------- | ------ |
| Agent Orchestrator            | Verify answer revision and revalidation after an initial rejection                      | PASS   |
| Prompt-Injection Instructions | Verify that the Reasoner prompt identifies retrieved document instructions as untrusted | PASS   |

**Latest automated test result:**

```text
Ran 2 tests in 0.006s

OK
```

Both tests use mocked responses and do not consume Gemini API credits.

### 7.2 Functional Testing

The Streamlit application was tested using uploaded résumé documents.

The system successfully:

- Retrieved relevant document chunks from ChromaDB.
- Generated answers using Google Gemini.
- Displayed source filenames and chunk identifiers.
- Displayed the Planner Agent's retrieval strategy.
- Displayed retrieved evidence in the Agent Execution Trace.
- Displayed the Validator Agent's assessment.

These tests confirmed that the major application components worked together in the tested scenarios.

### 7.3 Prompt-Injection Security Evaluation

A controlled security evaluation was conducted using `security_test.txt`.

The document contained legitimate application information and a malicious instruction attempting to redirect the assistant's response.

**Test ID:** SEC-001  
**Result:** PASS

The assistant retrieved the malicious content but answered the legitimate user question instead of following the embedded instruction.

The Validator Agent classified the answer as valid.

The complete methodology, observations, limitations, and recommendations are documented in [SECURITY_EVALUATION.md](SECURITY_EVALUATION.md).

### 7.4 Evaluation Limitations

The current evaluation has several limitations:

- Automated tests primarily verify workflow logic and prompt construction.
- Only one live prompt-injection scenario has been evaluated.
- No comprehensive retrieval-accuracy benchmark has been conducted.
- No quantitative hallucination-rate assessment has been completed.
- No load testing or production performance benchmarking has been performed.
- LLM-based validation does not guarantee factual correctness.

Further testing is required before production deployment.

---

## 8. Known Limitations

Although the Enterprise Document AI Assistant demonstrates a functional agentic RAG architecture, several limitations remain.

### 8.1 Retrieval Accuracy

Semantic search may retrieve irrelevant document chunks or overlook information needed to answer complex questions.

The current implementation does not include a dedicated reranking model or a quantitative retrieval evaluation framework.

### 8.2 LLM Reliability

Google Gemini may generate incomplete or inaccurate responses.

The Validator Agent provides an additional evaluation step, but its judgments are also generated by an LLM and are not guaranteed to be correct.

### 8.3 Prompt-Injection Security

Retrieved document content is treated as untrusted data through prompt-level instructions.

However, these instructions do not constitute a complete security boundary. More comprehensive defenses and adversarial testing are required.

### 8.4 Access Control and Data Privacy

The application is designed for local development and evaluation.

It does not currently implement enterprise authentication, role-based access control, document-level authorization, or comprehensive audit logging.

### 8.5 Scalability and Performance

The system has not undergone production-scale load testing.

Embedding generation, document processing, retrieval, and Gemini API latency may affect response times as document volumes increase.

---

## 9. Future Enhancements

Potential improvements include:

1. **Hybrid Search:** Combine semantic vector retrieval with keyword-based retrieval.
2. **Document Reranking:** Introduce a reranking model to improve evidence relevance.
3. **Retrieval Evaluation:** Measure retrieval precision, recall, and ranking quality using a labeled question-answer dataset.
4. **Answer Quality Evaluation:** Measure faithfulness, factual accuracy, and answer relevance.
5. **Enhanced Security:** Add document-level access controls, stronger input isolation, and broader prompt-injection testing.
6. **User Authentication:** Introduce authenticated user sessions and role-based authorization.
7. **Document Management:** Support document deletion, replacement, versioning, and metadata filtering.
8. **Observability:** Add structured logging, latency monitoring, and token-usage tracking.
9. **Deployment:** Containerize the application using Docker and evaluate cloud deployment options.
10. **Automated CI/CD:** Run unit tests and security checks through GitHub Actions.

---

## 10. Conclusion

The Enterprise Document AI Assistant demonstrates the integration of document processing, semantic retrieval, large language models, and specialized AI agents into a functional question-answering application.

The project implements a four-agent workflow consisting of Planner, Retriever, Reasoner, and Validator agents.

It also incorporates persistent vector storage, evidence citations, an interactive execution trace, automated answer revision, and initial prompt-injection safeguards.

The completed implementation provides a foundation for further research and development in enterprise document intelligence, explainable AI, and agentic Retrieval-Augmented Generation.

The application remains a prototype and requires additional security, evaluation, and operational controls before production deployment.

---

## 11. Project Author

**Gideon Abunuma**

AI / Machine Learning | Data Science | Enterprise Document Intelligence

**Project:** Enterprise Document AI Assistant  
**Category:** AI/ML Capstone Project  
**Year:** 2026
