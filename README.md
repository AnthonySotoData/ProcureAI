# ProcureAI

<p align="center">

### AI-Powered Procurement & Contract Intelligence Platform

**FastAPI • Retrieval-Augmented Generation (RAG) • ChromaDB • OpenAI • Docker**

Transform procurement contracts into actionable business intelligence using semantic search and AI-powered analysis.

</p>

---

# Overview

ProcureAI is an enterprise-style AI application that enables procurement professionals to upload supplier agreements, purchasing contracts, and procurement documents, then analyze them using Retrieval-Augmented Generation (RAG).

Instead of manually reviewing lengthy contracts, users can ask natural-language questions and receive structured, citation-backed procurement intelligence generated from the source document.

---

# Key Features

- 📄 Upload procurement contracts
- 🧠 Semantic search using vector embeddings
- 🤖 AI-generated procurement analysis
- 📑 Citation-backed responses
- 🔍 Metadata-aware document retrieval
- 📊 Structured procurement reports
- ⚡ FastAPI REST API
- 🐳 Docker deployment
- ✅ Automated test suite

---

# System Architecture

> *(Architecture diagram coming in the next section.)*

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.12 |
| API | FastAPI |
| AI | OpenAI GPT-4.1-mini |
| Embeddings | SentenceTransformers |
| Vector Database | ChromaDB |
| PDF Processing | PyMuPDF |
| Validation | Pydantic |
| Testing | Pytest |
| Deployment | Docker |

---

# Example Workflow

1. Upload a procurement contract.
2. Extract and chunk the document.
3. Generate semantic embeddings.
4. Store vectors in ChromaDB.
5. Retrieve relevant contract sections.
6. Generate structured procurement analysis.
7. Return AI-generated results with citations.

---

# API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/documents/upload` | Upload procurement documents |
| `/documents/search` | Semantic contract search |
| `/analysis` | AI-powered procurement analysis |
| `/health` | Health check |

---

# Example Analysis Output

The AI can automatically generate:

- Executive Summary
- Supplier Obligations
- Buyer Responsibilities
- Deliverables
- Important Dates
- Pricing Terms
- Compliance Requirements
- Procurement Risks
- Missing Information
- Recommended Actions
- Confidence Score
- Source Citations

---

# Docker

```bash
docker compose build

docker compose up
```

Swagger:

```
http://localhost:8000/docs
```

---

# Future Enhancements

- Multi-document comparison
- Vendor scorecards
- Contract expiration alerts
- Cloud deployment
- Authentication
- CI/CD pipeline
- Azure OpenAI support
- Anthropic Claude support

---

# License

MIT
