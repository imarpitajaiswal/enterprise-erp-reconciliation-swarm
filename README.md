# 🧠 Enterprise ERP Reconciliation Swarm

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-Agentic_AI-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/LangChain-Orchestration-121D33?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Pinecone-Vector_DB-0066FF?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

> **Production-Grade Multi-Agent ERP Reconciliation Platform powered by Agentic AI, LangGraph, and Retrieval-Augmented Generation (RAG).**

An enterprise AI system that autonomously reconciles procurement transactions, validates compliance policies, performs ERP ledger verification, and orchestrates multi-agent decision making with fault-tolerant workflow execution.

---

# 📖 Overview

Enterprise ERP systems process thousands of procurement transactions every day. Detecting inconsistencies across invoices, purchase orders, compliance policies, and financial ledgers typically requires multiple teams and manual verification.

Traditional automation struggles whenever contextual reasoning or regulatory validation is required.

The **Enterprise ERP Reconciliation Swarm** addresses this challenge through an **Agentic AI architecture** that coordinates specialized AI agents capable of routing reconciliation tasks, querying enterprise databases, retrieving policy knowledge through Retrieval-Augmented Generation (RAG), and maintaining resilient execution state across long-running workflows.

Built with **FastAPI**, **LangGraph**, **Groq**, **Pinecone**, **SQLAlchemy**, and **Docker**, the platform demonstrates enterprise-scale AI orchestration using modular, production-oriented design principles.

---

# 🎯 Business Objectives

The platform is designed to:

- Automate ERP reconciliation workflows
- Detect procurement discrepancies
- Validate compliance policies
- Reduce manual audit effort
- Maintain secure policy retrieval
- Support scalable enterprise deployments

---

# 🏗 System Architecture

```text
                Procurement Event
                        │
                        ▼
              FastAPI API Gateway
                        │
                        ▼
          LangGraph Supervisor Agent
                        │
      ┌─────────────────┴──────────────────┐
      ▼                                    ▼
 ERP Ledger Agent                  Compliance Agent
(SQLAlchemy)                    (Pinecone + RAG)
      │                                    │
      └─────────────────┬──────────────────┘
                        ▼
              Decision Aggregation
                        │
                        ▼
             Checkpoint Persistence
                        │
                        ▼
          Human Approval (Optional)
                        │
                        ▼
           Final Reconciliation Report
```

---

# 🤖 Multi-Agent Architecture

## Supervisor Agent

Acts as the orchestration layer responsible for:

- Task routing
- Workflow coordination
- State management
- Agent scheduling
- Decision aggregation

---

## ERP Ledger Agent

Responsible for:

- Querying ERP transactions
- Purchase order validation
- Invoice reconciliation
- Ledger verification
- Financial consistency checks

---

## Compliance Agent

Retrieves enterprise policies using RAG.

Responsibilities include:

- Semantic retrieval
- Policy validation
- Metadata filtering
- RBAC enforcement
- Context grounding

---

## Memory & Checkpoint Layer

Long-running workflows are checkpointed using LangGraph MemorySaver.

Benefits include:

- Fault tolerance
- Human approval workflows
- Execution recovery
- Persistent conversation state

---

# 🔐 Secure Retrieval Pipeline

Unlike conventional RAG systems, retrieved documents are filtered **before** reaching the language model.

Metadata filters include:

- Department
- Clearance Level
- Policy Category
- Access Permissions

Only authorized policy chunks are injected into the prompt, helping reduce unnecessary context exposure.

---

# ⚙️ Technology Stack

| Layer | Technology |
|---------|------------|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| LLM Provider | Groq (Llama 3.3 70B) |
| Vector Database | Pinecone |
| Embeddings | all-MiniLM-L6-v2 |
| Database | SQLAlchemy + SQLite |
| Deployment | Docker / Render |

---

# ✨ Engineering Highlights

- Agentic AI Workflows
- LangGraph State Machines
- Multi-Agent Collaboration
- Retrieval-Augmented Generation (RAG)
- Role-Based Context Retrieval
- Async FastAPI Backend
- Enterprise API Design
- Stateful Workflow Recovery
- Production-Oriented Architecture
- Cloud-Native Deployment

---

# 🚀 Local Deployment

## Clone Repository

```bash
git clone https://github.com/imarpitajaiswal/enterprise-erp-reconciliation-swarm.git
cd enterprise-erp-reconciliation-swarm
```

## Create Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

```env
GROQ_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=erp-compliance
DATABASE_URL=sqlite+aiosqlite:///./erp_enterprise.db
```

> Configure the Pinecone index with **384 dimensions** using the **cosine similarity** metric.

## Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

## Run Integration Tests

```bash
python -m scripts.verify_swarm
```

---

# 📊 Enterprise Readiness

The platform incorporates several production-oriented design considerations.

### Fault-Tolerant Execution

- Workflow checkpointing
- Execution recovery
- Human approval support

### Asynchronous Processing

- Non-blocking FastAPI architecture
- Concurrent request handling
- Low-latency inference

### Secure Retrieval

- Metadata-based filtering
- RBAC enforcement
- Context isolation

### Scalability

- Stateless API layer
- Modular agent architecture
- Containerized deployment
- Horizontal scaling support

---

# 💼 Business Applications

Potential enterprise use cases include:

- ERP Reconciliation
- Procurement Compliance
- Financial Audit Automation
- Internal Policy Validation
- Enterprise Knowledge Retrieval
- SAP Workflow Automation

---

# 📈 Future Roadmap

- Human-in-the-Loop Dashboard
- Multi-LLM Routing
- MCP Integration
- LangSmith Observability
- Redis Semantic Cache
- Kafka Event Streaming
- PostgreSQL Production Backend
- Kubernetes Deployment

---

# 🎓 Skills Demonstrated

This project showcases experience with:

- Agentic AI
- LangGraph
- Multi-Agent Systems
- Enterprise RAG
- FastAPI
- Pinecone
- Prompt Engineering
- Async Python
- Enterprise AI Architecture
- Cloud-Native AI Systems

---

# 👩‍💻 Author

## Arpita Jaiswal

**AI Engineer | Generative AI | Agentic AI Systems | Enterprise AI Architecture**

Building production-ready AI systems using Large Language Models, Retrieval-Augmented Generation (RAG), Agentic AI, and cloud-native engineering principles.

### Connect

🌐 Portfolio: https://arpita-portfolio-puce.vercel.app

💻 GitHub: https://github.com/imarpitajaiswal

💼 LinkedIn: https://linkedin.com/in/imarpitajaiswal

✍️ Medium: https://medium.com/@imarpitajaiswal

𝕏 X: https://x.com/imarpitajaiswal
