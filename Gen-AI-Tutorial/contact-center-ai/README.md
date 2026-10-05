# Contact-Center AI — 3-Day Interview Sprint

A production-style Contact-Center AI system supporting chat/voice with RAG, MCP tools, and agentic orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Chat/Voice)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────▼─────────────┐
         │  Intent Router Agent      │
         │  (LangChain/LangGraph)    │
         └─────────────┬─────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    ▼                  ▼                  ▼
┌─────────┐      ┌───────────┐     ┌──────────┐
│ Docs RAG│      │ DB Lookup │     │API Tools │
│(Pinecone│      │(MongoDB)  │     │  (MCP)   │
│+ FAISS) │      └───────────┘     └──────────┘
└────┬────┘
     │
     ▼
┌──────────────────────────┐
│ Grounding & Confidence   │
│ Guardrails               │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Response + Citations     │
│ Conversation Memory      │
└────────┬─────────────────┘
         │
         ▼
   Output (Chat/Voice)
```

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| LLM | OpenAI gpt-4 | Production-grade, Fast inference |
| Vector DB | Pinecone + FAISS | Hybrid: managed scaleability + local speed |
| Primary DB | MongoDB | Flexible schema, multi-tenant config |
| Orchestration | LangGraph + LangChain Agents | DAGs for workflows, agents for agentic loops |
| Embeddings | text-embedding-3-small | Fast, cheap, good quality |
| Reranker | BGE-reranker-large | Gold standard cross-encoder |

## 3-Day Sprint Roadmap

### **Day 1: RAG Foundation**
- [ ] Document ingestion pipeline (chunking strategies)
- [ ] Embed and index to Pinecone + FAISS
- [ ] Hybrid retrieval (vector + BM25)
- [ ] Reranking (top-50 → top-5)
- [ ] QA chain with grounding and citations
- **Interview Prep**: Chunking rationale, reranking impact, failure modes

### **Day 2: Agentic + MCP**
- [ ] Intent router agent
- [ ] MCP tools: docsRAG, dbLookup, policyCheck, ticketCreate
- [ ] Tool governance layer (schema, allowlist, timeouts)
- [ ] Conversation memory + state envelope
- [ ] LangGraph orchestration example
- **Interview Prep**: Tool control, context passing, agent coordination

### **Day 3: Hardening + Admin + Drills**
- [ ] Guardrails: refusal, groundedness, fallback
- [ ] Latency optimizations (caching, parallelization)
- [ ] Admin config panel mockup
- [ ] Mock interview drills (tough Q&A)
- **Interview Prep**: Failure modes, observability, tradeoffs

## First 5 Intents (MVP)

1. **My account details** → DB lookup + policy check
2. **Balance** → DB lookup with formatting
3. **Network Issue** → Docs RAG + troubleshooting guide
4. **Bill pay** → DB lookup + API tool
5. **FAQs** → Semantic search on docs

## Getting Started

```bash
# 1. Clone and setup
cd contact-center-ai
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# 2. Configure env
cp .env.example .env
# Add your API keys

# 3. Run Day 1 exercises
python notebooks/day1_ingestion.py
python notebooks/day1_retrieval.py
```

## Key Papers & References

- **RAG**: Retrieval Augmented Generation for Knowledge-Intensive NLP (Facebook AI)
- **Reranking**: Cross-Encoder Architecture for Ranking
- **MCP**: Model Context Protocol (Anthropic)
- **LangGraph**: Stateful multi-agent orchestration

---

**Interview Mantra**: "I don't just use RAG, I understand when and how it fails."
