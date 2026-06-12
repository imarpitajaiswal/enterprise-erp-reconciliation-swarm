# 🧠 Cognitive ERP Reconciliation Swarm

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/v0.1/docs/langgraph/)
[![Groq](https://img.shields.io/badge/Groq_Llama_3.3-f55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white)](https://www.pinecone.io/)
[![Cloud Deployment](https://img.shields.io/badge/Render_Live_Status-Deployed-success?style=for-the-badge&logo=render)](https://render.com/)

**Live API Endpoint (Swagger UI):** [LIVE_RENDER_URL](https://erp-reconciliation-engine.onrender.com/docs)

## 📊 Executive Summary
Supply chain procurement anomalies and ERP ledger mismatches cost large enterprises millions annually. Standard automation breaks when context is required, and traditional RAG pipelines fail in regulated environments due to hallucination and lack of strict access control. 

The **Cognitive ERP Reconciliation Swarm** is an autonomous, fault-tolerant multi-agent state machine. It is designed to ingest asynchronous procurement payloads, query mock SAP databases, and cross-reference enterprise compliance policies using a Zero-Trust Vector pipeline to resolve discrepancies without human intervention.

## 🏗️ System Architecture

This engine operates on a scalable, decoupled agentic network:

1. **The Executive Router (Supervisor Node):** A LangGraph-orchestrated traffic controller powered by Groq's Llama-3.3-70B. It evaluates incoming JSON payloads and dynamically shifts execution state to the appropriate domain specialist.
2. **The Ledger Auditor (ERP Node):** Interfaces directly with an asynchronous SQLite backend (`aiosqlite`) to extract baseline transactional truths simulating an SAP HANA environment.
3. **The Compliance Specialist (Zero-Trust RAG Node):** Enforces strict Role-Based Access Control (RBAC). It utilizes local HuggingFace `all-MiniLM-L6-v2` embeddings (384-dimensional) mapped to a Pinecone vector database. Policy chunks are filtered by `clearance_level` and `department` *before* the context is fed to the LLM.
4. **Resilient Memory State:** Transactions are checkpointed mid-execution. If a payload is flagged for managerial override, the execution thread halts, waits for an asynchronous HTTP override trigger, and resumes exactly where it left off.

## 🛠️ Enterprise Tech Stack

| Domain | Technology | Implementation Detail |
| :--- | :--- | :--- |
| **Agentic Framework** | LangGraph & LangChain | StateGraph routing, MemorySaver checkpointing |
| **Reasoning Engine** | Groq (Llama-3.3-70b-versatile) | High-speed, high-tier logic execution |
| **Backend & Routing** | FastAPI & Uvicorn | Asynchronous endpoint orchestration, Middleware |
| **Vector Database** | Pinecone & HuggingFace | 384-dim semantic search with RBAC metadata filters |
| **Relational Database**| SQLAlchemy & aiosqlite | Async mock SAP ledger ingestion |
| **Deployment** | Render | Cloud-native containerized hosting |

---

## 🚀 Local Execution & Quickstart

Run the platform locally for development, testing, and architecture validation.

### 1. Clone the Repository

```bash
git clone https://github.com/imarpitajaiswal/enterprise-erp-reconciliation-swarm.git
cd enterprise-erp-reconciliation-swarm
```

### 2. Provision the Virtual Environment

```bash
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=erp-compliance
DATABASE_URL=sqlite+aiosqlite:///./erp_enterprise.db
ENV=development
```

> **Note:** Ensure your Pinecone index is configured with **384 dimensions** and the **cosine** similarity metric.

### 4. Start the FastAPI Engine

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Execute the End-to-End Integration Suite

Open a separate terminal and run:

```bash
python -m scripts.verify_swarm
```

This validates:

- Multi-agent orchestration
- State persistence and recovery
- Compliance workflow routing
- Tool invocation chains
- End-to-end reconciliation execution

---

## 📈 Scalability & Fault Tolerance Strategy

Designed to satisfy enterprise-grade requirements and large-scale corporate deployments.

### LLM Rate-Limit Mitigation

- Compatible with API Gateway token-bucket rate limiting.
- Implements exponential backoff and retry mechanisms.
- Supports resilient handling of Groq API HTTP 429 responses.

### Asynchronous Processing Architecture

- Built on FastAPI asynchronous execution patterns.
- Prevents request blocking during intensive inference operations.
- Maintains high throughput under concurrent workloads.

### Vector Search Optimization

- Designed for integration with Redis Semantic Cache.
- Reduces repetitive Pinecone retrieval operations.
- Minimizes embedding lookup latency and infrastructure costs.

### Enterprise Readiness

- Modular multi-agent architecture.
- Extensible workflow orchestration.
- Fault-tolerant state management.
- Production-ready API design.
- Cloud deployment compatible.

---

## 👩‍💻 Author

**Built by Arpita Jaiswal**

AI Engineer | GenAI Developer | Multi-Agent Systems Architect

Bridging AI Engineering with scalable enterprise impact through intelligent automation, retrieval-augmented systems, and production-grade Agentic AI solutions.
