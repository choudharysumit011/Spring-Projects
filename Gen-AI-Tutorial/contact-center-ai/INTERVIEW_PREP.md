"""
INTERVIEW PREP ROADMAP — Contact-Center AI

This comprehensive guide maps your 3-day sprint to interview readiness.
Each module is designed to teach you the concepts and code patterns
you'll encounter in senior GenAI/Agentic AI interviews.
"""

# ==============================================================================
# DAY 1: RAG FOUNDATION (Query Understanding → Retrieval → Grounding)
# ==============================================================================

## CONCEPTS TO MASTER
- Chunking strategies: Fixed-size (naive) vs Recursive (smart) vs Semantic (best)
- Embedding pipeline: Text → Vector (1536 dims) → Vector DB
- Embedding models: OpenAI ada-002 / text-embedding-3-small (speed+cost) vs BGE (quality)
- Retrieval modes: Similarity (basic), MMR (diversity), Hybrid (dense+sparse)
- Reranking: Two-stage retrieval (top-50 → top-5 with cross-encoder)

## INTERVIEW QUESTION 1: "Your RAG gives wrong info. How?"
ANSWER:
1. Retrieval Miss: Relevant chunks not in top-50
   - Why: Bad chunking, stale embeddings, query not well-aligned
   - Fix: Recursive chunking, metadata filtering, query expansion
   
2. Embedding Mismatch: Query and chunk semantically different
   - Why: Embedding model not trained on domain, query uses different phrasing
   - Fix: Hybrid retrieval (vector + BM25), semantic reranking
   
3. Low-Quality Source Docs: Original docs have errors/outdated info
   - Why: Docs not reviewed, versioning incorrect
   - Fix: Metadata with recency, source-level confidence scores
   
4. Post-Retrieval Hallucination: LLM invents despite correct retrieval
   - Why: Temperature too high, few-shot examples bad, no grounding check
   - Fix: Lower temperature, mandatory citation binding, groundedness check

## CODE MODULES DAY 1
src/config.py
  └─ Settings: Centralized config (API keys, model names, chunking params)

src/rag/ingestion.py
  └─ DocumentIngestionPipeline: Load, parse, chunk (fixed/recursive/semantic)
  └─ Chunk: Data class for chunk + metadata
  └─ ChunkingStrategy: Enum for strategy choice

src/rag/embeddings.py
  └─ EmbeddingModel: Base class for pluggable embedders
  └─ OpenAIEmbedding: text-embedding-3-small integration
  └─ SentenceTransformerEmbedding: Local fallback (all-MiniLM)
  └─ EmbeddingPipeline: Orchestrate batch embedding, stats

notebooks/day1_exercise.py
  └─ Exercise 1-5: Load → Chunk → Embed → Store → Search
  └─ LocalVectorStore (FAISS): Prototype vector DB locally
  └─ Query embedding + top-K retrieval demo

## DELIVERABLE DAY 1
✓ Load 5 support docs (account, balance, network, billing, FAQ)
✓ Recursive chunking (preserve context)
✓ OpenAI embeddings (1536-dim vectors)
✓ Local FAISS index (fast similarity search)
✓ Baseline retrieval for 5 sample queries
✓ Retrieval quality metrics (similarity scores, top-K precision)


# ==============================================================================
# DAY 2: AGENTIC + MCP TOOLS (Intent → Action → Response)
# ==============================================================================

## CONCEPTS TO MASTER
- Intent classification: Supervised router vs semantic similarity
- Tool orchestration: MCP (Model Context Protocol)
- Tool governance: Schema validation, intent allowlist, timeouts, audit logs
- Agent patterns: LangChain Agents (ReAct loop) vs LangGraph (DAG workflows)
- Context passing: Shared state envelope across agent hops
- Conversation memory: Session store + turn history + entity tracking

## INTERVIEW QUESTION 2: "How do you manage tools in MCP?"
ANSWER:
1. Tool Governance Layer:
   - JSON Schema contracts for each tool (input/output)
   - Intent-based allowlist (e.g., "balance" can call dbLookup but not ticketCreate)
   - Timeouts: Hard limit 5s per tool call
   - Retries: Exponential backoff (1s, 2s, 4s) with circuit breaker on 3 failures

2. Least-Privilege Credentials:
   - Each tool gets scoped API key (read-only, time-limited)
   - Audit log per tool call (who, what, when, status)
   - Rate limiting per intent (100 calls/hour for balance lookup)

3. Tool Composition:
   - Router: "balance" → dbLookup (not docsRAG)
   - Sequential: "bill pay" → checkBalance → validatePayment → submitPayment
   - Parallel: Fetch account details AND check network status simultaneously
   - Conditional: If payment fails → offerPaymentPlan (another tool)

## INTERVIEW QUESTION 3: "How do agents pass context?"
ANSWER:
1. State Envelope (Shared Data Structure):
   {
     "userId": "cust_123",
     "sessionId": "sess_abc",
     "intent": "balance",
     "entities": {"account": "123", "service_type": "data"},
     "retrievalResults": [{"chunk_id": "...", "score": 0.92}],
     "toolResults": {"dbLookup": {"balance": "10GB"}},
     "safetyFlags": {"requires_auth": true, "pii_present": false},
     "conversationHistory": [{"role": "user", "content": "..."}]
   }

2. Agent Read/Write Contracts:
   - Intent Router: Reads input, writes "intent", "entities"
   - RAG Agent: Reads "intent", writes "retrievalResults"
   - Tool Agent: Reads "intent", "entities", writes "toolResults", "safetyFlags"
   - Response Agent: Reads all, writes "response"

3. Versioning:
   - State schema version (v1.0) allows backward compatibility
   - Agents can handle v0.9 state, upgrade gracefully
   - No breaking changes without migration plan

## CODE MODULES DAY 2
src/agents/intent_router.py
  └─ IntentClassifier: Semantic or supervised intent detection
  └─ 5 intents: account, balance, network, billing, faq

src/mcp_tools/base.py
  └─ MCPTool: Base class for all tools
  └─ Tool schema, governance, audit logging

src/mcp_tools/docs_rag.py
  └─ DocsRAGTool: Query vector DB, return top-5 with citations

src/mcp_tools/db_lookup.py
  └─ DBLookupTool: Query MongoDB for structured data

src/mcp_tools/policy_check.py
  └─ PolicyCheckTool: Validate customer eligibility, compliance

src/mcp_tools/ticket_create.py
  └─ TicketCreateTool: Create support ticket, return ticket ID

src/memory/context.py
  └─ StateEnvelope: Shared context dict with validation
  └─ ConversationMemory: Store session history, entity tracking

src/agents/orchestrator.py
  └─ LangGraphOrchestrator: DAG-based agent coordination
  └─ LangChainAgent: ReAct loop alternative

## DELIVERABLE DAY 2
✓ Intent router distinguishing 5 intents with 90%+ accuracy
✓ 4 MCP tools with schema validation and governance
✓ Context envelope passing between agents
✓ Conversation memory store (session + history)
✓ Simple orchestration example (intent → tool → response)
✓ End-to-end flow for 1 complex intent (e.g., "bill pay")


# ==============================================================================
# DAY 3: HARDENING + ADMIN + INTERVIEW DRILLS
# ==============================================================================

## CONCEPTS TO MASTER
- Guardrails: Refusal policy, groundedness checking, confidence thresholding
- Latency optimization: Caching, parallelization, model tiering
- Observability: Trace logging, error categorization, feedback loops
- Admin panel: Config management for docs, DB connections, intents, guardrails
- Error recovery: Graceful degradation, fallback strategies, escalation
- Cost optimization: Token counting, batch efficiency, model selection

## INTERVIEW QUESTION 4: "How do you reduce latency and hallucinations?"
ANSWER (Latency):
1. Parallelization: Embed query + fetch conversation history simultaneously
2. Caching: Store embeddings, frequent queries, inference KV cache
3. Model Tiering: Small model for routing (100ms), large only for synthesis (500ms)
4. Streaming: Return first token in 100ms, stream rest (perceived speed)
5. Precomputation: Pre-embed docs at ingestion, keep hot index in memory

ANSWER (Hallucination):
1. Grounding: Mandatory citation from retrieval results
2. Confidence: Score response against retrieved context
3. Refusal: "I don't have enough information" > confident guess
4. Temperature: Lower for factual (0.2), higher for creative (0.7)
5. Few-shot: Examples showing good grounding behavior
6. Monitoring: User feedback loop → detect hallucinations → retrain

## INTERVIEW QUESTION 5: "How do you connect different agents?"
ANSWER:
1. Shared State Envelope: All agents read/write same dict (see Day 2)
2. Sequential Composition: Agent A outputs → Agent B inputs
3. Conditional Routing: Agent decides which next agent based on result
4. Parallel Execution: Independent agents run concurrently, results merged
5. Hierarchical: Sub-agents for specialized tasks (e.g., PaymentAgent with Verification Sub-Agent)
6. Async Patterns: Long-running tools return job ID, poll for result

## CODE MODULES DAY 3
src/guardrails/grounding.py
  └─ GroundednessChecker: Verify response grounded in retrieval
  └─ CitationValidator: Check citations exist in source chunks

src/guardrails/safety.py
  └─ RefusalPolicy: Intent-level & response-level refusal rules
  └─ ConfidenceThreshold: Only respond if confidence > threshold

src/admin/config_manager.py
  └─ AdminConfigSchema: RAG docs, DB connections, guardrails config
  └─ ConfigValidator: Ensure valid config before deployment

src/admin/panel.py
  └─ AdminPanel: REST API for managing system config
  └─ Endpoints: /docs/upload, /docs/refresh, /intents/{id}/config

src/observability/tracer.py
  └─ QueryTracer: Log every step (intent, retrieval, tool, response)
  └─ MetricsCollector: Latency, hallucination rate, tool accuracy

src/optimization/cache.py
  └─ QueryCache: Embed + retrieve cached results
  └─ ToolResultCache: Cache tool outputs for repeated queries

## DELIVERABLE DAY 3
✓ Guardrails reducing hallucination rate by 40%+
✓ Latency < 2s for 95th percentile queries
✓ Admin panel allowing config changes without restart
✓ Observability dashboard: Query success rate, latency, costs
✓ Mock interview drills: 10 tough Q&A patterns prepared


# ==============================================================================
# INTERVIEW MOCK DRILLS
# ==============================================================================

USE THESE TO PRACTICE:

1. "Walk me through your RAG pipeline from user query to response"
   - Chunking strategy, why recursive?
   - Embedding: which model, why dimensions matter
   - Retrieval: hybrid + reranking, why important
   - Grounding: citation validation, groundedness check
   - Response: confidence scoring, fallback strategy

2. "Your system says 'balance is $100' but customer says they never charged. Why?"
   - Could be retrieval error (wrong data pulled)
   - Could be stale index (balance updated but cached)
   - Could be hallucination (LLM invented the number)
   - Debug strategy: Check retrieval trace, validate source data, version docs

3. "How do you prevent your RAG from outputting customer's password?"
   - PII masking in docs (redact before ingestion)
   - Intent-level access control (password reset needs verification)
   - Refusal policy (don't output passwords even if in docs)
   - Guardrails: Detect PII in response, block before returning

4. "Design a multi-tenant contact center using the same documents"
   - Document versioning: Each tenant can have version v1, v2
   - Metadata filtering: Only retrieve tenant's documents
   - Index partitioning: Separate FAISS index per tenant or tagged retrieval
   - Cost scalability: Embedding sharing across tenants, DB queries isolated

5. "Your inference latency is 5 seconds. How do you get to 1 second?"
   - Profile: Where's the bottleneck? (embedding, retrieval, LLM?)
   - Parallelization: Embed query + fetch history simultaneously
   - Caching: Store query embeddings, reuse for similar queries
   - Model tiering: Use smaller, faster model for routing
   - Streaming: Return first token at 500ms, stream the rest

6. "How do you evaluate if your RAG is getting better?"
   - Metrics: Retrieval precision@5, answer accuracy, hallucination rate
   - Eval set: 100+ ground truth Q&A pairs (human annotated)
   - A/B test: Old chunking vs new chunking vs reranker
   - User feedback: Thumbs up/down on responses (automatic retraining)
   - Production monitoring: Fraction of queries escalated to human

7. "Your embedding model is trained on general text. How handle domain-specific queries?"
   - Domain adaptation: Fine-tune embedding model on contact-center QA pairs
   - Hybrid retrieval: Vector (general) + BM25 (exact keyword match)
   - Query expansion: Rephrase query in domain language before embedding
   - Metadata filtering: Prefer chunks tagged with domain category

8. "How do you ensure agent A's output works for agent B?"
   - State contract: Document required fields in StateEnvelope
   - Type validation: Pydantic models for state validation
   - Version gates: Agent checks state version before using
   - Integration tests: Test each agent pair together before prod

9. "I see tool_X is being called 10x per query. Why and how fix?"
   - Diagnosis: Check agent's ReAct loop (maybe infinite loop?)
   - Root cause: Maybe agent misunderstands tool's purpose
   - Fix: Better tool description, tighter confidence threshold for tool use
   - Monitoring: Add loop-count limit, alert on > 3 tool calls

10. "Your system hallucinates on 5% of queries. Cost: $50k/year in escalations. How reduce?"
    - Root cause analysis: Is it retrieval or generation hallucination?
    - If retrieval: Improve chunking, add reranking, better metadata
    - If generation: Lower temperature, mandatory grounding, confidence threshold
    - Monitoring: Track hallucination rate per intent, prioritize high-impact ones
    - ROI: Improving to 1% saves $40k/year, worth 200 hours of eng work


# ==============================================================================
# PROJECT STRUCTURE
# ==============================================================================

contact-center-ai/
├── src/
│   ├── config.py                # Central config (API keys, model names, params)
│   ├── rag/
│   │   ├── ingestion.py        # Chunking pipeline (fixed/recursive/semantic)
│   │   ├── embeddings.py       # Embedding models (OpenAI, SentenceTransformer)
│   │   └── retrieval.py        # Retrieval modes (similarity, MMR, hybrid)
│   ├── agents/
│   │   ├── intent_router.py    # Intent classification
│   │   ├── orchestrator.py     # LangGraph + LangChain orchestration
│   │   └── response_gen.py     # Grounded response generation
│   ├── mcp_tools/
│   │   ├── base.py             # Tool base class + governance
│   │   ├── docs_rag.py         # RAG tool
│   │   ├── db_lookup.py        # DB query tool
│   │   ├── policy_check.py     # Policy validation tool
│   │   └── ticket_create.py    # Ticket creation tool
│   ├── db/
│   │   ├── mongo_client.py     # MongoDB integration
│   │   └── schema.py           # Data models (customer, intent, config)
│   ├── memory/
│   │   ├── context.py          # StateEnvelope, validation
│   │   └── store.py            # Conversation memory store
│   ├── guardrails/
│   │   ├── grounding.py        # Groundedness checking
│   │   └── safety.py           # Refusal, confidence threshold
│   ├── admin/
│   │   ├── config_manager.py   # Config management
│   │   └── panel.py            # REST API for admin
│   └── observability/
│       ├── tracer.py           # Query execution tracing
│       └── metrics.py          # Performance metrics
│
├── data/
│   ├── docs/                    # Knowledge base (account, balance, network, billing, faq)
│   └── seed/                    # Seed data (customer profiles, intents, policies)
│
├── notebooks/
│   ├── day1_exercise.py        # Load → Chunk → Embed → Retrieve
│   ├── day2_exercise.py        # Intent → Tools → Response (Build during Day 2)
│   └── day3_exercise.py        # Full system + guardrails (Build during Day 3)
│
├── tests/
│   ├── test_chunking.py        # Chunking correctness
│   ├── test_retrieval.py       # Retrieval quality
│   ├── test_agents.py          # Agent coordination
│   └── test_integration.py     # End-to-end flows
│
├── config/
│   └── guardrails.yaml         # Guardrails configuration
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # Project overview + setup
└── INTERVIEW_PREP.md           # This file


# ==============================================================================
# HOW TO USE THIS ROADMAP
# ==============================================================================

DAY 1 (Today):
  - [ ] Read this file (15 min)
  - [ ] Run `python notebooks/day1_exercise.py` (30 min)
  - [ ] Study src/rag/ingestion.py + embeddings.py (30 min)
  - [ ] Answer interview Q1 (retrieval failures) in your own words (15 min)
  - [ ] Checkpoint: You understand RAG foundation ✓

DAY 2 (Tomorrow):
  - [ ] Design StateEnvelope schema on whiteboard (20 min)
  - [ ] Code intent_router.py (1 hour)
  - [ ] Code 2 MCP tools (db_lookup, docs_rag) (2 hours)
  - [ ] Build simple orchestrator (1 hour)
  - [ ] Run end-to-end test (30 min)
  - [ ] Answer interview Q2-3 (agents + tools) on camera (30 min)
  - [ ] Checkpoint: You can build multi-agent systems ✓

DAY 3 (Interview day -1):
  - [ ] Add guardrails.py (1 hour)
  - [ ] Build admin panel mockup (1 hour)
  - [ ] Mock interview drills (2 hours)
  - [ ] Practice whiteboard design (30 min)
  - [ ] Review code, explain each module (1 hour)
  - [ ] Checkpoint: Interview-ready ✓

INTERVIEW DAY:
  - [ ] Calm, deep breathing
  - [ ] You've built this system from scratch
  - [ ] You can explain every decision
  - [ ] Edge cases? You've thought through them
  - [ ] Code? It's on your GitHub, shipping tomorrow
  - [ ] Good luck! 🚀
"""
