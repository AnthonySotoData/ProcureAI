# ProcureAI

ProcureAI is an AI-powered procurement intelligence platform that uses retrieval-augmented generation to analyze supplier agreements and procurement documents.

The application combines semantic search, structured metadata, and large language models to produce grounded procurement insights, including obligations, pricing terms, compliance requirements, risks, missing information, and recommended actions.

## Architecture

![ProcureAI Architecture](images/procureai_architecture.svg)

## Key Features

- Upload and index procurement contracts through a FastAPI endpoint
- Extract and intelligently chunk PDF documents
- Generate semantic embeddings using SentenceTransformers
- Store and retrieve contract knowledge with ChromaDB
- Filter retrieval results using procurement metadata
- Analyze contract obligations, dates, pricing, compliance, and risks
- Produce structured AI responses with confidence scores
- Return source citations for traceability
- Support both OpenAI and mock LLM providers
- Run consistently through Docker and Docker Compose
- Validate application behavior with automated tests

## Technology Stack

| Category | Technologies |
|---|---|
| API | FastAPI, Uvicorn |
| AI | OpenAI GPT-4.1-mini |
| Retrieval | ChromaDB, SentenceTransformers |
| Document Processing | PyMuPDF |
| Validation | Pydantic |
| Testing | Pytest |
| Deployment | Docker, Docker Compose |
| Language | Python 3.12 |

## Application Demonstration

### Interactive REST API

ProcureAI exposes documented REST endpoints for system health, document ingestion, semantic search, and AI-powered procurement analysis.

![ProcureAI Swagger API](images/swagger.png)

### Procurement Document Ingestion

Procurement documents are uploaded with structured metadata such as supplier, contract number, document type, department, and contract dates. The document is then extracted, chunked, embedded, and stored in ChromaDB.

![ProcureAI Document Upload](images/upload-endpoint.png)

### Semantic Contract Retrieval

The semantic search endpoint retrieves the most relevant contract sections based on meaning rather than exact keyword matching. Each result includes source metadata for traceability.

![ProcureAI Semantic Search](images/semantic-search.png)

### AI-Generated Procurement Intelligence

The analysis endpoint combines retrieved contract context with a structured procurement prompt to produce grounded insights, including supplier obligations, important dates, pricing terms, compliance requirements, procurement risks, missing information, recommended actions, confidence, and citations.

![ProcureAI AI Analysis](images/ai-analysis.png)

## Retrieval-Augmented Generation Workflow

1. A procurement document is uploaded through the API.
2. Text is extracted from each PDF page.
3. The text is divided into retrieval-ready chunks.
4. SentenceTransformer embeddings are generated.
5. Chunks and metadata are stored in ChromaDB.
6. A user submits a procurement question or analysis request.
7. ProcureAI retrieves the most relevant contract sections.
8. Retrieved context is added to the analysis prompt.
9. The language model generates a structured response.
10. Source citations are returned with the analysis.

This architecture keeps generated responses grounded in the uploaded procurement documentation.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Application information |
| `GET` | `/health` | Health check |
| `POST` | `/documents/upload` | Upload and index a procurement document |
| `POST` | `/documents/search` | Perform semantic contract search |
| `POST` | `/analysis` | Generate structured procurement intelligence |

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/AnthonySotoData/ProcureAI.git
cd ProcureAI