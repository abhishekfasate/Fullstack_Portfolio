#!/usr/bin/env python
"""
One-time script to add 15 blog posts covering AI, ML, Development, and Tech topics.
Run from the backend/ directory:

    python scripts/add_blogs.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, init_db
from app.models.blog import BlogPost, Tag

# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------
TAG_DEFS = [
    ("Artificial Intelligence", "artificial-intelligence"),
    ("Machine Learning", "machine-learning"),
    ("Web Development", "web-development"),
    ("DevOps", "devops"),
    ("Python", "python"),
    ("JavaScript", "javascript"),
    ("Cloud Computing", "cloud-computing"),
    ("Cybersecurity", "cybersecurity"),
    ("System Design", "system-design"),
    ("New Tech", "new-tech"),
]

# ---------------------------------------------------------------------------
# Blog posts  (title, slug, excerpt, content, reading_time, featured, tag_names)
# ---------------------------------------------------------------------------
POSTS = [
    # 1 -----------------------------------------------------------------------
    (
        "Understanding Large Language Models: How GPT and Claude Actually Work",
        "understanding-large-language-models",
        "A deep dive into the transformer architecture, attention mechanisms, and training pipelines that power today's most capable AI assistants.",
        """## Introduction

Large Language Models (LLMs) have transformed the technology landscape in a way that few innovations have managed to do in the past decade. Tools like ChatGPT, Claude, Gemini, and LLaMA are no longer academic curiosities — they are deployed in production systems, embedded in IDEs, powering customer support, writing code, and assisting in medical research. Yet despite their ubiquity, most developers interact with them as black boxes. This post pulls back the curtain.

## What is a Transformer?

The transformer architecture, introduced in the landmark 2017 paper *Attention Is All You Need* by Vaswani et al., is the foundation of every modern LLM. Before transformers, sequence models relied on Recurrent Neural Networks (RNNs) and LSTMs, which processed tokens one at a time from left to right. This sequential nature made them slow to train and prone to forgetting long-range dependencies.

Transformers broke this bottleneck by processing all tokens in a sequence simultaneously using a mechanism called **self-attention**.

### Self-Attention Explained

Self-attention allows each token in a sequence to look at every other token and decide how much to "attend" to it. Consider the sentence:

> "The animal didn't cross the street because **it** was too tired."

To resolve what "it" refers to, a model needs to connect "it" with "animal," not "street." Self-attention assigns high weights between "it" and "animal" and low weights between "it" and "street."

Mathematically, attention is computed as:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

Where Q (Query), K (Key), and V (Value) are linear projections of the input embeddings. The dot product `QK^T` measures similarity between tokens, `sqrt(d_k)` prevents vanishing gradients, and the softmax converts raw scores into a probability distribution.

### Multi-Head Attention

Rather than computing attention once, transformers compute it multiple times in parallel — each time with different learned projections. This is called **multi-head attention**. Different heads can specialize: one might track syntactic relationships, another semantic ones, another coreference.

## Tokenization

Before any computation happens, raw text is converted to tokens. GPT-4 uses Byte-Pair Encoding (BPE), which builds a vocabulary of subword units by iteratively merging the most frequent adjacent pairs. The word "unbelievable" might become ["un", "believ", "able"] — three tokens. Tokenization affects cost (API pricing is per token), model behavior, and even language fairness.

## Pre-training

LLMs are trained on massive corpora — trillions of tokens scraped from the web, books, code repositories, and scientific papers. The objective is simple: **predict the next token**. This is called a causal language model objective (or autoregressive training).

Despite the simplicity, next-token prediction forces the model to learn grammar, facts, reasoning patterns, and even social norms implicitly. It's a form of self-supervised learning — no human labels are needed.

Training at this scale requires thousands of GPUs running for months. GPT-3 was trained on 45 TB of text using 10,000 V100 GPUs. The energy cost alone is staggering.

## Fine-tuning and RLHF

A pre-trained LLM knows a lot about language but doesn't know how to *behave helpfully*. This is addressed through fine-tuning:

1. **Supervised Fine-Tuning (SFT):** Human trainers write example conversations showing the desired behavior. The model is fine-tuned to mimic these.
2. **Reward Model Training:** A separate model is trained to score responses (preferring helpful, harmless, honest ones).
3. **RLHF (Reinforcement Learning from Human Feedback):** The LLM is fine-tuned using the reward model as a signal, via Proximal Policy Optimization (PPO).

This pipeline is what turns a raw language model into an assistant that refuses harmful requests, admits uncertainty, and maintains a coherent personality.

## Context Windows and Memory

A key limitation of LLMs is the **context window** — the maximum number of tokens they can process at once. GPT-3.5 had 4k tokens; GPT-4 Turbo goes up to 128k; Claude 3 supports up to 200k. Longer context windows allow models to reason over entire codebases, books, or lengthy conversations.

However, attention is O(n²) in sequence length, so longer contexts are significantly more expensive to compute. Techniques like sparse attention, sliding windows, and rotary positional embeddings (RoPE) help mitigate this.

## Emergent Capabilities

One of the most surprising findings in LLM research is **emergence** — capabilities that appear abruptly as model scale increases, not gradually. Chain-of-thought reasoning, multi-step arithmetic, and in-context learning were not explicitly trained; they emerged from scale.

This has led researchers to question whether current evaluation benchmarks are adequate, and whether we fully understand what these models can and cannot do.

## Practical Implications for Developers

- **Prompt engineering matters**: How you phrase a question dramatically affects output quality. Techniques like few-shot prompting, chain-of-thought, and system prompts are now core developer skills.
- **RAG (Retrieval-Augmented Generation)**: LLMs don't update their weights at inference time. To give them fresh or private information, pair them with a vector database.
- **Hallucination is a feature of the architecture**: The model generates plausible continuations — it doesn't "look things up." Always validate critical outputs.
- **Cost management**: Token usage adds up fast. Use smaller models for classification tasks, reserve frontier models for complex reasoning.

## Conclusion

LLMs are not magic — they are the result of elegant mathematics, massive compute, and careful human feedback. Understanding the underlying mechanics makes you a better user, a better prompter, and a better engineer when building on top of them. The transformer revolution is far from over; new architectures, training paradigms, and applications appear every month. Stay curious.
""",
        18,
        True,
        ["Artificial Intelligence", "Machine Learning", "New Tech"],
    ),
    # 2 -----------------------------------------------------------------------
    (
        "Building Production-Ready REST APIs with FastAPI: A Complete Guide",
        "building-production-ready-rest-apis-fastapi",
        "Learn how to build scalable, secure, and well-documented REST APIs using FastAPI — from project structure and authentication to async database access and deployment.",
        """## Introduction

FastAPI has rapidly become one of the most popular Python web frameworks, and for good reason. It delivers Django-level features with Flask-level simplicity, adds automatic OpenAPI documentation, and leverages Python's type hints to provide editor autocomplete and runtime validation out of the box. In this guide, we build a production-ready API from scratch.

## Why FastAPI?

Compared to Flask and Django REST Framework, FastAPI offers:

- **Automatic docs**: Swagger UI and ReDoc generated from your code, zero configuration.
- **Native async support**: Built on Starlette and compatible with asyncio from day one.
- **Pydantic validation**: Request bodies and query params are automatically validated and serialized.
- **Speed**: On par with Node.js and Go in benchmarks, thanks to uvicorn and async I/O.
- **Type safety**: Full IDE support, reducing bugs at development time.

## Project Structure

A well-organized FastAPI project for production:

```
app/
├── main.py               # App factory, router registration
├── core/
│   ├── config.py         # Pydantic Settings from .env
│   ├── database.py       # SQLAlchemy async engine
│   └── security.py       # JWT, password hashing
├── api/
│   └── v1/
│       └── endpoints/    # Route modules
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic request/response models
└── services/             # Business logic layer
```

Never put business logic in route handlers. Keep routes thin — they should only parse input, call a service, and return output.

## Async Database Access with SQLAlchemy

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
```

Use `asyncpg` as the driver (`postgresql+asyncpg://...`). The `pool_pre_ping=True` ensures stale connections are detected before use — critical in production.

## Authentication with JWT

```python
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> str:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload["sub"]
```

Pair this with a FastAPI dependency that extracts the token from the `Authorization: Bearer` header and injects the current user into route handlers.

## Request Validation with Pydantic

```python
from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```

FastAPI will automatically return a 422 Unprocessable Entity with detailed error messages if validation fails — no extra code needed.

## Background Tasks and Celery

For long-running operations (sending emails, processing uploads, syncing external APIs), use Celery with Redis:

```python
from celery import Celery

celery = Celery("worker", broker=settings.CELERY_BROKER_URL)

@celery.task
def send_welcome_email(user_email: str):
    # ... email logic
    pass

# In your route handler:
send_welcome_email.delay(user.email)
```

This keeps your API response times fast by offloading work to background workers.

## Rate Limiting

Use `slowapi` (a FastAPI-compatible port of Flask-Limiter):

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    ...
```

## Error Handling

Define custom exception handlers globally:

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code},
    )
```

This gives clients consistent error shapes regardless of where the error originates.

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Never use `allow_origins=["*"]` in production if your API uses cookies or credentials.

## Deployment with Docker and Nginx

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

Put Nginx in front as a reverse proxy. It handles TLS termination, request buffering, and static file serving far more efficiently than uvicorn.

## Conclusion

FastAPI is a joy to work with and scales well from side projects to high-traffic production services. The combination of async I/O, Pydantic validation, automatic docs, and Python's rich ecosystem makes it a compelling choice for any new API project. The patterns shown here — layered architecture, JWT auth, Celery workers, Docker deployment — are battle-tested and will serve you well at scale.
""",
        16,
        True,
        ["Web Development", "Python"],
    ),
    # 3 -----------------------------------------------------------------------
    (
        "Docker and Kubernetes: Containerization from Zero to Production",
        "docker-kubernetes-containerization-guide",
        "A comprehensive walkthrough of containerizing applications with Docker and orchestrating them at scale with Kubernetes — covering real-world patterns used in production.",
        """## Introduction

Ten years ago, deploying software meant logging into a server, manually installing dependencies, and praying that the environment matched your laptop. Today, containers have made that process reproducible, portable, and automated. Docker and Kubernetes are now the default infrastructure layer for most cloud-native applications. This post walks through both — from first principles to production patterns.

## What is a Container?

A container is a lightweight, isolated process that shares the host OS kernel but has its own filesystem, network, and process space. Unlike virtual machines, containers don't include a full OS — they package only the application and its dependencies. This makes them:

- **Fast to start**: Milliseconds, not minutes.
- **Lightweight**: Tens of MB, not GB.
- **Consistent**: "Works on my machine" becomes "works everywhere."

## Docker Fundamentals

### Writing a Dockerfile

```dockerfile
# Use slim base image to reduce attack surface and image size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Non-root user for security
RUN adduser --disabled-password appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Layer Caching

Docker builds images layer by layer. Each instruction creates a layer. If a layer hasn't changed, Docker reuses the cached version. This is why you copy `requirements.txt` and install dependencies before copying the rest of the code — changing your app code won't invalidate the dependency installation layer.

### Multi-Stage Builds

For compiled languages or frontend apps:

```dockerfile
# Stage 1: Build
FROM node:20 AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

The final image contains only the compiled output and Nginx — not Node.js or your source code.

## Docker Compose for Local Development

```yaml
version: "3.9"
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://app:secret@db:5432/appdb
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  pgdata:
```

This gives every developer an identical, reproducible environment with a single `docker-compose up`.

## Kubernetes: Orchestration at Scale

Docker Compose is great for local dev, but it can't handle failover, auto-scaling, rolling deployments, or multi-node clusters. Kubernetes (K8s) does all of this.

### Core Concepts

- **Pod**: The smallest deployable unit. Usually one container, sometimes a sidecar pattern.
- **Deployment**: Manages a set of identical Pods with desired replica count and rolling update strategy.
- **Service**: A stable network endpoint (DNS name + IP) that load-balances across Pods.
- **Ingress**: Routes external HTTP/S traffic to Services based on hostname/path rules.
- **ConfigMap / Secret**: Inject configuration and credentials into Pods without baking them into images.

### A Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: ghcr.io/myorg/backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
```

Always define `resources.requests` and `resources.limits`. Without them, a runaway pod can starve other workloads on the same node.

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

K8s will automatically add pods when CPU exceeds 70% and remove them when demand drops.

## CI/CD Integration

A typical GitHub Actions pipeline:

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/myorg/backend:${{ github.sha }}

- name: Deploy to Kubernetes
  run: |
    kubectl set image deployment/backend \
      backend=ghcr.io/myorg/backend:${{ github.sha }}
    kubectl rollout status deployment/backend
```

Rolling deployments ensure zero downtime — K8s brings up new pods before terminating old ones.

## Conclusion

Containers have fundamentally changed how software is built and deployed. Docker makes packaging applications consistent and portable. Kubernetes makes running them at scale reliable and automated. Together, they form the backbone of modern cloud-native infrastructure. Start with Docker Compose locally, graduate to Kubernetes when you need scale and resilience.
""",
        17,
        False,
        ["DevOps", "Cloud Computing", "New Tech"],
    ),
    # 4 -----------------------------------------------------------------------
    (
        "Retrieval-Augmented Generation (RAG): Building AI Apps That Know Your Data",
        "retrieval-augmented-generation-rag-guide",
        "RAG combines the reasoning power of LLMs with the precision of search. Learn how to build a production RAG pipeline using vector databases, embeddings, and LangChain.",
        """## Introduction

Large Language Models are trained on static snapshots of the internet. They don't know what happened yesterday, they don't have access to your private documents, and they can't read your company's internal knowledge base. Retrieval-Augmented Generation (RAG) solves this by giving LLMs a dynamic memory: a search system that retrieves relevant context at query time and injects it into the prompt.

## The Problem RAG Solves

Consider asking an LLM "What was the outcome of our Q3 board meeting?" The model has no access to your internal documents. Even if it did, confidential data should never be baked into a public model's weights.

RAG sidesteps this entirely: store your documents in a searchable database, retrieve the most relevant chunks when a query arrives, and pass them to the LLM as context. The model reasons over real data without ever being fine-tuned on it.

## Core Components

### 1. Document Ingestion

Raw documents (PDFs, HTML pages, Markdown files, database records) are split into smaller chunks and stored.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\\n\\n", "\\n", ". ", " "],
)
chunks = splitter.split_text(raw_document_text)
```

Chunk size is a critical hyperparameter. Too large and retrieval is noisy. Too small and individual chunks lack context. 512-1024 tokens with ~10% overlap is a common starting point.

### 2. Embedding Generation

Each chunk is converted to a dense vector (embedding) using an embedding model. Semantically similar texts produce similar vectors.

```python
from openai import OpenAI

client = OpenAI()

def embed(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    return response.data[0].embedding
```

### 3. Vector Database Storage

Embeddings are stored in a vector database that supports approximate nearest neighbor (ANN) search.

Popular choices:
- **pgvector**: PostgreSQL extension. Great if you already use Postgres.
- **Pinecone**: Managed, serverless. Easy to start.
- **Weaviate**: Open-source, rich metadata filtering.
- **Qdrant**: Fast, Rust-based, excellent for self-hosting.
- **ChromaDB**: Lightweight, local-first, great for prototyping.

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docs")

collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=[embed(c) for c in chunks],
)
```

### 4. Retrieval

At query time, embed the user's question and search for the most similar document chunks.

```python
query = "What are the refund policies?"
query_embedding = embed(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
)
context = "\\n\\n".join(results["documents"][0])
```

### 5. Generation

Inject the retrieved context into the LLM prompt:

```python
prompt = f'''You are a helpful assistant. Use only the context below to answer the question.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {query}
Answer:'''

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
)
print(response.choices[0].message.content)
```

## Advanced Techniques

### Hybrid Search

Pure vector search misses exact keyword matches. Hybrid search combines dense (semantic) and sparse (BM25/TF-IDF) retrieval, then uses Reciprocal Rank Fusion to merge results.

### Re-ranking

A cross-encoder re-ranker (e.g., Cohere Rerank) takes the top-N retrieved chunks and re-scores them with higher precision before passing to the LLM.

### Metadata Filtering

Filter by document source, date, department, or user permissions before semantic search. This prevents retrieval from crossing security boundaries.

### Query Rewriting

Use an LLM to rewrite ambiguous queries before retrieval. "Tell me more" becomes "What are the key features of Product X mentioned earlier in the conversation?"

## Evaluating RAG Pipelines

Key metrics:
- **Context Precision**: Are the retrieved chunks actually relevant?
- **Context Recall**: Did we retrieve all relevant chunks?
- **Faithfulness**: Does the answer actually come from the retrieved context?
- **Answer Relevancy**: Does the answer address the question?

Tools like **RAGAS** automate this evaluation.

## Production Considerations

- **Chunking strategy matters enormously**: Hierarchical chunking (document → section → paragraph) with parent-child retrieval often outperforms flat chunking.
- **Embedding model drift**: If you switch embedding models, you must re-embed your entire corpus.
- **Latency budget**: Retrieval + embedding + LLM call chains add up. Cache frequent queries.
- **Observability**: Log queries, retrieved chunks, and answers. You can't improve what you can't measure.

## Conclusion

RAG is now the standard architecture for building LLM applications that need to work with private, dynamic, or domain-specific knowledge. It's more reliable than fine-tuning for factual tasks, cheaper to update, and provides the citations users need to trust AI outputs. The components are mature and production-ready — there's no reason not to use RAG in your next AI application.
""",
        19,
        True,
        ["Artificial Intelligence", "Machine Learning", "Python"],
    ),
    # 5 -----------------------------------------------------------------------
    (
        "React 18 Deep Dive: Concurrent Rendering, Suspense, and Server Components",
        "react-18-concurrent-rendering-suspense-server-components",
        "React 18 introduced the most significant architectural changes to the library since hooks. This post unpacks concurrent rendering, automatic batching, Suspense, and the new Server Components model.",
        """## Introduction

React 18 wasn't just a minor version bump — it was a fundamental rethinking of how React renders UI. The headline feature, **concurrent rendering**, enables React to interrupt, pause, and resume rendering work, making applications more responsive under heavy load. Combined with Server Components, Suspense improvements, and automatic batching, React 18 changes how we think about data fetching, code splitting, and performance.

## Concurrent Rendering

In React 17 and earlier, rendering was **synchronous and blocking**. Once React started rendering a tree, it had to finish before the browser could do anything else — respond to user input, animate, update the DOM. This caused "jank" on complex UIs.

React 18's concurrent mode makes rendering **interruptible**. React can now:

- Start rendering a component tree
- Pause when the browser needs to handle input
- Resume or abandon the render based on priority

This is entirely opt-in and transparent to most application code. You don't rewrite your components — you use the new hooks and APIs that signal to React which updates are urgent.

### useTransition

`useTransition` marks a state update as non-urgent, allowing urgent updates (like typing) to interrupt it:

```tsx
const [isPending, startTransition] = useTransition();

function handleSearch(query: string) {
  setInputValue(query); // Urgent: update the input immediately

  startTransition(() => {
    setSearchResults(filterData(query)); // Non-urgent: can be interrupted
  });
}
```

If the user types faster than results update, React will abandon in-progress renders of the results and start fresh with the latest query. No stale results, no janky UI.

### useDeferredValue

For cases where you don't control the state update (e.g., a value from a parent):

```tsx
const deferredQuery = useDeferredValue(query);
// Use deferredQuery for expensive rendering, query for the input
```

## Automatic Batching

In React 17, state updates inside async callbacks (setTimeout, fetch, promises) were not batched — each caused a separate re-render. React 18 automatically batches all updates regardless of context:

```tsx
// React 17: 2 renders
// React 18: 1 render (automatic batching)
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
}, 1000);
```

This is a significant performance win requiring zero code changes.

## Suspense for Data Fetching

Suspense has been in React since 16.6 but was limited to code splitting. React 18 expands it to data fetching with first-class support in frameworks like Next.js and Remix.

```tsx
function UserProfile({ userId }: { userId: string }) {
  const user = use(fetchUser(userId)); // throws a Promise if not ready
  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<Skeleton />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

The `use()` hook (still experimental in 18, stable in 19) allows components to "suspend" while data is loading. The nearest Suspense boundary renders the fallback. No `isLoading` booleans, no conditional renders.

### Streaming SSR with Suspense

React 18 enables **streaming server-side rendering**. Instead of waiting for all data to load before sending HTML, the server can stream the shell immediately and progressively inject content as it becomes available:

```tsx
// app/page.tsx (Next.js App Router)
export default function Page() {
  return (
    <main>
      <Header />
      <Suspense fallback={<PostsSkeleton />}>
        <BlogPosts /> {/* Streamed after initial HTML */}
      </Suspense>
    </main>
  );
}
```

This dramatically improves Time to First Byte (TTFB) and Largest Contentful Paint (LCP).

## React Server Components (RSC)

Server Components are a paradigm shift. They render exclusively on the server and send serialized UI to the client — no JavaScript bundle shipped. They can:

- Access databases, file systems, and APIs directly
- Import large server-only libraries (pdf parsers, ORMs) without bundle impact
- Interleave with Client Components seamlessly

```tsx
// This component never ships to the browser
async function BlogPost({ slug }: { slug: string }) {
  const post = await db.query("SELECT * FROM posts WHERE slug = $1", [slug]);
  return <article>{post.content}</article>;
}
```

### Server vs Client Components

| Feature | Server Component | Client Component |
|---|---|---|
| useState / useEffect | No | Yes |
| Database access | Yes | No |
| Browser APIs | No | Yes |
| Ships to bundle | No | Yes |

Mark client components with `"use client"` at the top of the file. Everything else is a Server Component by default in the App Router.

## Performance Implications

The combination of concurrent rendering, streaming SSR, and Server Components creates a new performance ceiling:

- **Faster TTI**: Less JavaScript to parse and execute.
- **Better INP**: Concurrent rendering prevents long tasks from blocking interaction.
- **Improved LCP**: Streaming gets critical content to the screen sooner.
- **Smaller bundles**: Server Components keep heavy dependencies off the client.

## Conclusion

React 18 is a generational update. Concurrent rendering is already available to all applications through automatic batching and will be increasingly leveraged through `useTransition` and Suspense. Server Components represent the future of React — a model where the framework decides where code runs to optimize for performance and developer experience. Adopting the App Router in Next.js is the clearest path to using all these features today.
""",
        16,
        False,
        ["Web Development", "JavaScript", "New Tech"],
    ),
    # 6 -----------------------------------------------------------------------
    (
        "Cybersecurity Fundamentals Every Developer Must Know in 2025",
        "cybersecurity-fundamentals-developers-2025",
        "Security is not a checkbox — it's a discipline woven into every line of code. This guide covers the OWASP Top 10, secure coding practices, secrets management, and the developer's role in the security supply chain.",
        """## Introduction

The average cost of a data breach in 2024 was $4.88 million, and over 80% of breaches involved a human element — phishing, credential theft, or developer mistakes. Security is no longer the exclusive domain of a dedicated security team. Every developer who writes code that touches user data, handles authentication, or runs on a network is on the security team, whether they know it or not.

## OWASP Top 10: The Developer's Security Checklist

The Open Web Application Security Project maintains the Top 10 — the most critical web application security risks. Here are the ones most directly caused by developer code.

### 1. Injection (SQL, Command, LDAP)

**The attack**: User input is interpreted as code.

```python
# VULNERABLE: string interpolation in SQL
query = f"SELECT * FROM users WHERE email = '{user_input}'"

# SAFE: parameterized queries
query = "SELECT * FROM users WHERE email = $1"
result = await db.execute(query, user_input)
```

Never concatenate user input into SQL queries, shell commands, or LDAP filters. Always use parameterized queries or an ORM.

### 2. Broken Authentication

**The attack**: Weak passwords, predictable tokens, missing rate limiting.

Best practices:
- Use bcrypt/argon2 for password hashing (never MD5 or SHA-1 alone)
- Enforce MFA for admin accounts
- Rate limit login attempts (5 per minute per IP)
- Use short-lived JWT access tokens (15 min) with refresh token rotation
- Invalidate sessions on password change

### 3. Sensitive Data Exposure

**The attack**: PII, passwords, or keys transmitted or stored unencrypted.

- Always use HTTPS (TLS 1.2+). Redirect HTTP to HTTPS.
- Never log passwords, tokens, or credit card numbers.
- Encrypt sensitive database columns at rest.
- Use `SameSite=Strict` and `Secure` cookie flags.

### 4. Broken Access Control

**The attack**: Users can access resources or actions they shouldn't.

```python
# VULNERABLE: trusting user-supplied IDs
@router.get("/orders/{order_id}")
async def get_order(order_id: int, user: User = Depends(get_current_user)):
    return await db.get_order(order_id)  # Any user can access any order!

# SAFE: verify ownership
@router.get("/orders/{order_id}")
async def get_order(order_id: int, user: User = Depends(get_current_user)):
    order = await db.get_order(order_id)
    if order.user_id != user.id:
        raise HTTPException(status_code=403)
    return order
```

Always authorize at the resource level, not just the route level.

### 5. Security Misconfiguration

- Disable debug mode in production (`DEBUG=False`)
- Remove default credentials from all services
- Keep dependency versions updated (Dependabot / Renovate)
- Apply minimal permissions to service accounts (principle of least privilege)
- Never expose admin interfaces to the public internet

### 6. Cross-Site Scripting (XSS)

**The attack**: Injecting JavaScript into pages that execute in other users' browsers.

- Modern frameworks (React, Vue, Angular) escape HTML by default — don't use `dangerouslySetInnerHTML` with user input.
- Set `Content-Security-Policy` headers to restrict script sources.
- Use `HttpOnly` cookie flag to prevent JS from reading session cookies.

### 7. Insecure Dependencies

Your code is only as secure as your dependencies. Supply chain attacks (malicious npm packages, compromised PyPI packages) are increasingly common.

- Pin dependency versions in production.
- Run `npm audit` / `pip-audit` in CI.
- Use Dependabot or Snyk for automated vulnerability alerts.
- Review dependencies before installing them.

## Secrets Management

Secrets in source code are one of the most common causes of breaches. GitHub scans public repos and notifies providers when credentials are pushed — but private repos are not immune.

**Never do this:**
```python
OPENAI_API_KEY = "sk-real-key-here"  # Committed to git forever
```

**Do this instead:**
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

For production, use a secrets manager:
- **AWS Secrets Manager** / **Parameter Store**
- **HashiCorp Vault**
- **Doppler** (developer-friendly)
- **1Password Secrets Automation**

Rotate secrets regularly and immediately if compromised.

## Security Headers

Add these HTTP headers to every response:

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: no-referrer-when-downgrade
```

Use [securityheaders.com](https://securityheaders.com) to audit your site.

## Logging and Monitoring

You can't respond to what you can't see. Log authentication events, privilege escalations, and unusual access patterns. Set up alerts for:

- Multiple failed login attempts from the same IP
- Access to admin endpoints from unexpected IPs
- Unexpected large data exports
- Database queries with anomalous execution times (possible injection probing)

## Conclusion

Security is not about being paranoid — it's about building software that can be trusted. The practices here are not advanced; they are the baseline. Parameterized queries, proper password hashing, secret management, dependency auditing, and HTTPS are table stakes for any application that handles user data. Integrate security into your development workflow from day one, not as an afterthought before launch.
""",
        18,
        False,
        ["Cybersecurity", "Web Development"],
    ),
    # 7 -----------------------------------------------------------------------
    (
        "PostgreSQL Performance Tuning: Indexes, Query Plans, and Connection Pooling",
        "postgresql-performance-tuning-indexes-query-plans",
        "PostgreSQL is powerful but slow queries can cripple applications. Learn how to read EXPLAIN output, design effective indexes, avoid N+1 problems, and configure PgBouncer for connection pooling.",
        """## Introduction

PostgreSQL is one of the most capable open-source databases in existence. It handles complex queries, supports JSON, full-text search, geospatial data, and extensibility that most developers never fully explore. But with great power comes great responsibility — a single missing index or a naive ORM query can bring an application to its knees under load. This guide covers the tools and techniques to keep Postgres fast.

## Understanding EXPLAIN ANALYZE

Every performance investigation starts with `EXPLAIN ANALYZE`. It shows the query plan Postgres chose and the actual execution statistics.

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT p.title, COUNT(c.id) as comment_count
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.published = true
GROUP BY p.id, p.title
ORDER BY comment_count DESC
LIMIT 20;
```

Key things to look for:

- **Seq Scan**: Reading every row in the table. Fine for small tables, catastrophic for large ones.
- **Index Scan**: Using an index. Usually what you want.
- **Hash Join vs Nested Loop**: Hash joins are better for large result sets; nested loops for small ones.
- **Rows**: Compare estimated vs actual row counts. Large discrepancies mean stale statistics — run `ANALYZE`.
- **Buffers**: How many pages were read from cache vs disk. High disk reads → you need more `shared_buffers` or better indexes.

## Index Strategies

### B-Tree Indexes (Default)

Good for equality, range queries, and sorting:

```sql
CREATE INDEX idx_posts_published_created
ON posts (published, created_at DESC)
WHERE published = true; -- Partial index: only indexes published posts
```

Partial indexes are smaller and faster when you always filter on a condition.

### Composite Indexes: Column Order Matters

```sql
-- Query: WHERE user_id = $1 AND created_at > $2
CREATE INDEX idx_orders_user_created ON orders (user_id, created_at);
-- user_id first: can also serve WHERE user_id = $1 alone
-- created_at first: CANNOT serve WHERE user_id = $1 alone
```

Put the most selective (highest cardinality) or equality-filtered column first.

### Covering Indexes (Index-Only Scans)

```sql
-- Query only needs id, title, created_at
CREATE INDEX idx_posts_covering
ON posts (published, created_at DESC)
INCLUDE (id, title);
```

Adding `INCLUDE` columns lets Postgres satisfy the query entirely from the index without visiting the heap.

### GIN Indexes for Arrays and JSONB

```sql
-- Full-text search
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', content));

-- JSONB containment queries
CREATE INDEX idx_metadata ON products USING GIN(metadata);
```

### Index Bloat

Indexes grow with updates and deletes. Monitor bloat with:

```sql
SELECT schemaname, tablename, indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

Use `REINDEX CONCURRENTLY` to rebuild bloated indexes without locking.

## Avoiding N+1 Queries

The N+1 problem is the most common ORM-related performance issue.

**N+1 (bad)**:
```python
posts = await db.execute(select(Post))
for post in posts.scalars():
    # Executes a new query for EVERY post!
    comments = await db.execute(select(Comment).where(Comment.post_id == post.id))
```

**Eager loading (good)**:
```python
from sqlalchemy.orm import selectinload

posts = await db.execute(
    select(Post).options(selectinload(Post.comments))
)
```

SQLAlchemy's `selectinload` fetches all related records in one additional query, not N queries.

## Connection Pooling with PgBouncer

Every database connection consumes ~5-10 MB of memory and requires a process on the Postgres side. A web server with 100 workers × 10 connections each = 1000 Postgres connections. Postgres struggles above a few hundred connections.

PgBouncer sits between your app and Postgres, maintaining a small pool of real connections and multiplexing thousands of application connections through them.

```ini
# pgbouncer.ini
[databases]
myapp = host=postgres port=5432 dbname=myapp

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

**Pool modes:**
- `session`: One real connection per client session. Simple but doesn't help much.
- `transaction`: Real connection held only during a transaction. Most common.
- `statement`: Real connection held only during a single statement. Requires no transactions.

Transaction pooling reduces real connections by 10-50x typically.

## Configuration Tuning

Default Postgres config is intentionally conservative. Key settings to tune:

```
# Memory (set to 25% of RAM)
shared_buffers = 2GB

# Query planner (set to 75% of RAM)
effective_cache_size = 6GB

# Per-sort/hash operation memory
work_mem = 64MB

# Checkpoint frequency (reduce I/O spikes)
checkpoint_completion_target = 0.9
wal_buffers = 64MB

# Query planning
random_page_cost = 1.1  # For SSDs (default 4.0 assumes spinning disks)
```

## Monitoring

Tools for ongoing visibility:
- **pg_stat_statements**: Built-in extension tracking query execution stats.
- **pgBadger**: Log analyzer generating beautiful HTML reports.
- **Prometheus + postgres_exporter**: Metrics for Grafana dashboards.

```sql
-- Top 10 slowest queries
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Conclusion

PostgreSQL performance is largely about giving the query planner the information and resources it needs to make good decisions. That means proper indexes, up-to-date statistics, appropriate memory settings, and keeping the planner's row count estimates accurate. Start with `EXPLAIN ANALYZE` on your slowest queries — the answers are almost always there.
""",
        17,
        False,
        ["Web Development", "Python", "System Design"],
    ),
    # 8 -----------------------------------------------------------------------
    (
        "Machine Learning in Production: From Jupyter Notebook to Deployed Model",
        "machine-learning-production-deployment-guide",
        "Training a model is 10% of the work. This guide covers the other 90%: feature stores, model registries, serving infrastructure, monitoring, and the MLOps practices that keep production ML healthy.",
        """## Introduction

The joke in the ML community is that 90% of machine learning happens in Jupyter notebooks and never ships to production. The other 10% causes production incidents. This guide is about bridging that gap — taking a model from a notebook to a reliable, monitored, scalable production service.

## The ML Production Gap

A notebook is an exploration environment. It has hard-coded file paths, uses the analyst's local Python environment, processes data in a specific order that depends on cell execution history, and has no error handling. None of that is acceptable in production.

The gap between notebook and production involves:

1. **Reproducibility**: The same code on different machines should produce the same results.
2. **Scalability**: The model must handle production traffic volume.
3. **Monitoring**: Is the model still performing well? Has the data distribution shifted?
4. **Reliability**: Failed predictions should fail gracefully, not crash the app.
5. **Auditability**: What version of the model made this prediction, trained on what data?

## Feature Engineering at Scale

Notebook ML often processes raw features in the training loop. Production ML separates this into a **feature store** — a centralized repository of computed features that serves both training and inference.

Why this matters: If your training pipeline computes "user's average purchase value over the last 30 days" differently from your inference pipeline, you get **training-serving skew** — the model sees different data at inference than it was trained on. This silently degrades performance.

Popular feature stores: **Feast** (open-source), **Tecton** (managed), **Hopsworks**, or even a Redis + PostgreSQL combination for simpler use cases.

## Experiment Tracking with MLflow

Never lose track of what worked and what didn't:

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

with mlflow.start_run():
    mlflow.log_params({
        "n_estimators": 200,
        "max_depth": 10,
        "random_state": 42,
    })

    model = RandomForestClassifier(n_estimators=200, max_depth=10)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
```

MLflow tracks parameters, metrics, artifacts, and source code for every experiment run. You can compare runs, reproduce any experiment, and register models for deployment.

## Model Serving

### Option 1: REST API with FastAPI

```python
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = joblib.load("model.pkl")

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(request: PredictionRequest):
    prediction = model.predict([request.features])
    return {"prediction": int(prediction[0])}
```

Good for custom logic, preprocessing, business rules.

### Option 2: BentoML

BentoML abstracts serving infrastructure. Define a service, and BentoML handles batching, adaptive concurrency, and deployment to cloud platforms:

```python
import bentoml
from bentoml.io import NumpyNdarray

runner = bentoml.sklearn.get("credit_model:latest").to_runner()
svc = bentoml.Service("credit_service", runners=[runner])

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def predict(input_data):
    return runner.predict.run(input_data)
```

### Option 3: Managed Services

- **AWS SageMaker**: End-to-end ML platform. High operational overhead but fully managed.
- **Vertex AI (GCP)**: Strong for TensorFlow and AutoML workloads.
- **Azure ML**: Deep enterprise integration.
- **Modal**: Serverless GPU inference, excellent developer experience.

## Monitoring: The Critical Missing Piece

Most ML teams monitor system metrics (latency, error rate) but miss the ML-specific signals that matter:

### Data Drift

The statistical distribution of input features shifts over time. A fraud detection model trained on pre-COVID spending patterns performs poorly post-COVID.

Tools: **Evidently AI**, **WhyLogs**, **Arize Phoenix**

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=training_df, current_data=production_df)
report.save_html("drift_report.html")
```

### Concept Drift

The relationship between features and the target changes. User behavior shifts, regulations change, or the world just evolves. Concept drift requires retraining.

### Prediction Monitoring

Log every prediction with its input, output, timestamp, and model version. When ground truth becomes available, compute and alert on performance degradation.

## Retraining Pipelines

A production ML system needs automated retraining:

1. Collect new labeled data
2. Run data quality checks
3. Retrain model (on new data + historical data)
4. Evaluate against holdout set and compare to current production model
5. If improved, register new model version
6. Deploy via canary (5% traffic → 50% → 100%) monitoring for regressions

Tools: **Apache Airflow**, **Prefect**, **Metaflow**, **Kubeflow Pipelines**

## A/B Testing Models

Never deploy a new model to 100% of traffic immediately. Use A/B testing:

- Route 5% of traffic to the new model
- Compare business metrics (conversion rate, revenue, user retention) — not just accuracy
- Use statistical significance testing before declaring a winner
- Roll back automatically if error rate spikes

## Conclusion

Production ML is a software engineering discipline as much as a data science one. The skills that matter — reproducibility, observability, reliability, CI/CD — are the same skills that matter in any production software system. The difference is that your production artifact (the model) decays over time as the world changes, requiring a new discipline: ongoing monitoring and retraining. Build this infrastructure from the start, not after your first production incident.
""",
        20,
        True,
        ["Machine Learning", "Artificial Intelligence", "Python", "DevOps"],
    ),
    # 9 -----------------------------------------------------------------------
    (
        "System Design Interview: How to Design a URL Shortener Like Bit.ly",
        "system-design-url-shortener-bitly",
        "Walk through the complete system design of a production URL shortener — covering requirements, database design, hashing strategies, caching, and scaling to billions of requests.",
        """## Introduction

URL shorteners seem deceptively simple — take a long URL, return a short one, redirect when visited. Yet designing one that handles billions of redirects per day with sub-10ms latency is a rich systems problem that touches databases, caching, hashing, load balancing, and global distribution. This is one of the most common system design interview questions for a reason.

## Requirements Gathering

Always start with clarifying questions:

**Functional requirements:**
- Given a long URL, return a unique short URL.
- Redirect short URL to original URL.
- Custom aliases? Expiration dates? Analytics?

**Non-functional requirements (assumed):**
- 100M new URLs created per day
- 10B redirects per day (100:1 read/write ratio)
- 99.99% availability (53 min downtime per year maximum)
- Redirect latency < 10ms (p99)
- URLs stored for 5 years

**Back-of-envelope:**
- 10B redirects/day = ~115,000 requests/second
- 100M URLs/day × 5 years × 365 = 182B URLs
- Each URL record ~500 bytes → 91 TB storage

## API Design

```
POST /api/shorten
Body: { "long_url": "https://...", "custom_alias": "mylink", "expiry_days": 30 }
Response: { "short_url": "https://bit.ly/abc123" }

GET /{short_code}
Response: 301 Redirect to long URL
```

Use **301 (Permanent)** if you never need to change the target. Use **302 (Temporary)** if you want browsers to always ask your server (required for analytics).

## Generating Short Codes

### Option 1: MD5 / SHA-256 Hash + Truncate

Hash the long URL, take the first 7 characters:

```python
import hashlib
import base64

def generate_short_code(long_url: str) -> str:
    hash_bytes = hashlib.md5(long_url.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes)[:7].decode()
```

**Problem**: Collisions. Two different URLs can produce the same 7-character prefix. You'd need collision detection and retry logic.

### Option 2: Base62 Encoding of Auto-Increment ID

Use a distributed ID generator (Twitter Snowflake, database sequence) and encode in base62 (a-z, A-Z, 0-9):

```python
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def encode_base62(num: int) -> str:
    result = []
    while num > 0:
        result.append(CHARS[num % 62])
        num //= 62
    return "".join(reversed(result))
```

7 characters in base62 = 62^7 ≈ 3.5 trillion unique codes. No collisions by design.

**Problem**: Auto-increment IDs are predictable (enumerable). Use a random shuffle or counter obfuscation if you need to prevent enumeration.

### Option 3: Pre-generated Code Pool

Generate millions of random codes in advance, store them in a queue (Redis), pop one when needed. No collision risk, no sequential patterns. Good for very high write throughput.

## Database Design

### URL Table

```sql
CREATE TABLE urls (
    id          BIGINT PRIMARY KEY,
    short_code  VARCHAR(10) UNIQUE NOT NULL,
    long_url    TEXT NOT NULL,
    user_id     BIGINT,
    created_at  TIMESTAMP DEFAULT NOW(),
    expires_at  TIMESTAMP,
    click_count BIGINT DEFAULT 0
);

CREATE INDEX idx_urls_short_code ON urls (short_code);
```

The `short_code` index is the only query path for redirects — keep it highly optimized.

### Database Choice

- **For reads** (115K RPS): This is too much for a single database. Use **read replicas** or a distributed database like **CockroachDB**.
- **For writes** (1,150 RPS): A single primary Postgres can handle this easily.

## Caching Strategy

Redirects are pure reads of a small piece of data. Cache aggressively.

```
Request → Load Balancer → App Server → Redis Cache → Database
                                    (cache miss only)
```

```python
import redis
import json

r = redis.Redis()

async def resolve_short_code(code: str) -> str | None:
    # Check cache first
    cached = r.get(f"url:{code}")
    if cached:
        return cached.decode()

    # Cache miss: query database
    url = await db.fetchrow("SELECT long_url FROM urls WHERE short_code = $1", code)
    if url:
        r.setex(f"url:{code}", 86400, url["long_url"])  # Cache for 24h
        return url["long_url"]
    return None
```

With a 99% cache hit rate, your database only sees 1% of redirect traffic = ~1,150 RPS.

## Analytics

Tracking every click at 115K RPS is challenging. Options:

1. **Async write**: Write to a Kafka queue; Flink/Spark consumers aggregate and persist.
2. **Approximate counting**: Use Redis HyperLogLog for unique visitor counts.
3. **Batch processing**: Write to a columnar store (ClickHouse, BigQuery) optimized for analytics queries.

Never write to your main URL database on every redirect — it'll become a bottleneck.

## Handling Scale: Global Distribution

For worldwide sub-10ms latency, you need **edge deployment**:

- Deploy redirect service in multiple regions (US, EU, Asia)
- Use **GeoDNS** to route users to the nearest region
- Cache URL mappings at the edge (Cloudflare Workers, Fastly)
- Eventual consistency is acceptable for URL records

## Handling Abuse

Short URL services are heavily abused for spam and phishing. Mitigations:
- Rate limit URL creation per IP and account
- Scan long URLs against Google Safe Browsing API
- Block known spam domains
- Flag URLs with anomalous click patterns

## Summary Architecture

```
Client → CDN (cache hit: 95%) → Load Balancer
                                      ↓ (cache miss)
                             App Servers (horizontal)
                                      ↓
                             Redis Cluster (cache)
                                      ↓ (cache miss)
                             Primary DB + Read Replicas
                                      ↓ (async)
                             Kafka → Analytics Pipeline
```

## Conclusion

A URL shortener evolves from a trivial CRUD app to a globally distributed, heavily cached, analytically rich system as requirements scale. The core insight is that redirects are pure reads of tiny data — optimize ruthlessly for that case. Cache at every layer, push reads to replicas and the edge, and handle writes asynchronously wherever possible.
""",
        19,
        False,
        ["System Design", "Web Development"],
    ),
    # 10 -----------------------------------------------------------------------
    (
        "TypeScript Advanced Patterns: Generics, Utility Types, and Type-Safe APIs",
        "typescript-advanced-patterns-generics-utility-types",
        "Go beyond basic TypeScript and learn the advanced type system features that make large codebases maintainable: generics, conditional types, mapped types, template literals, and type-safe API clients.",
        """## Introduction

TypeScript's type system is one of the most sophisticated of any mainstream language. Most developers use 20% of its power — basic interfaces, enums, and `as unknown as T` escape hatches. But the advanced features of TypeScript's type system can eliminate entire categories of runtime errors, generate types from runtime schemas, and make refactoring large codebases safe and confident. This post explores those features.

## Generics: Types as Parameters

Generics allow you to write code that works with any type while preserving type information.

```typescript
// Without generics: loses type information
function identity(arg: any): any {
  return arg;
}

// With generics: type is preserved
function identity<T>(arg: T): T {
  return arg;
}

const result = identity("hello"); // type: string, not any
```

### Generic Constraints

```typescript
interface HasId {
  id: number;
}

function findById<T extends HasId>(items: T[], id: number): T | undefined {
  return items.find(item => item.id === id);
}

// TypeScript knows the return type matches the input array's element type
const user = findById(users, 1); // type: User | undefined
```

### Generic Inference in React

```typescript
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [stored, setStored] = useState<T>(() => {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  const setValue = (value: T) => {
    setStored(value);
    window.localStorage.setItem(key, JSON.stringify(value));
  };

  return [stored, setValue];
}

// Usage — T is inferred as { theme: string; fontSize: number }
const [prefs, setPrefs] = useLocalStorage("prefs", { theme: "dark", fontSize: 14 });
```

## Utility Types

TypeScript ships with powerful built-in utility types.

### Partial, Required, Readonly

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

type UserUpdate = Partial<User>;       // All fields optional
type FrozenUser = Readonly<User>;      // All fields readonly
type RequiredUser = Required<User>;    // All fields required (removes ?)
```

### Pick and Omit

```typescript
type UserPreview = Pick<User, "id" | "name">;     // Only id and name
type UserWithoutId = Omit<User, "id">;             // Everything except id
```

### Record

```typescript
type RolePermissions = Record<"admin" | "editor" | "viewer", string[]>;

const permissions: RolePermissions = {
  admin: ["read", "write", "delete"],
  editor: ["read", "write"],
  viewer: ["read"],
};
```

## Conditional Types

Types that depend on other types — like ternary operators for types.

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<"hello">; // true
type B = IsString<42>;      // false

// Unwrap a Promise
type Awaited<T> = T extends Promise<infer U> ? U : T;
type Data = Awaited<Promise<User>>; // User
```

### Distributive Conditional Types

```typescript
type NonNullable<T> = T extends null | undefined ? never : T;

type Safe = NonNullable<string | null | undefined>; // string
```

## Mapped Types

Transform every property in a type:

```typescript
// Make all methods async
type Asyncify<T> = {
  [K in keyof T]: T[K] extends (...args: infer A) => infer R
    ? (...args: A) => Promise<R>
    : T[K];
};

// Make all properties optional and nullable
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K] | null;
};
```

## Template Literal Types

String manipulation at the type level:

```typescript
type EventName = "click" | "focus" | "blur";
type HandlerName = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

type ApiRoute = `/api/v1/${"users" | "posts" | "comments"}`;
// "/api/v1/users" | "/api/v1/posts" | "/api/v1/comments"
```

## Type-Safe API Clients

One of the most powerful applications: inferring client types from API schemas.

### With Zod

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  return UserSchema.parse(data); // Runtime validation + type narrowing
}
```

### With tRPC

tRPC generates fully type-safe API clients from server route definitions — no codegen step:

```typescript
// Server
const appRouter = router({
  getUser: publicProcedure
    .input(z.object({ id: z.number() }))
    .query(async ({ input }) => {
      return await db.users.findById(input.id);
    }),
});

// Client — fully typed, no manual type definitions needed
const user = await trpc.getUser.query({ id: 1 }); // type: User
```

## Discriminated Unions for State Machines

```typescript
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: string };

function render<T>(state: RequestState<T>) {
  switch (state.status) {
    case "idle":    return <div>Start a search</div>;
    case "loading": return <Spinner />;
    case "success": return <Results data={state.data} />;  // state.data is typed as T here
    case "error":   return <Error message={state.error} />; // state.error is typed as string here
  }
}
```

TypeScript narrows the type inside each case — you get autocomplete and type safety with no casts.

## Conclusion

TypeScript's advanced type system pays dividends at scale. Generics eliminate duplication while preserving type safety. Utility types make type transformations declarative. Conditional and mapped types let you derive types automatically from your runtime data models. Mastering these features means fewer runtime errors, more confident refactoring, and a codebase that documents itself through its types.
""",
        16,
        False,
        ["JavaScript", "Web Development"],
    ),
    # 11 -----------------------------------------------------------------------
    (
        "The Complete Guide to CI/CD Pipelines with GitHub Actions",
        "complete-guide-cicd-pipelines-github-actions",
        "Automate testing, building, and deployment with GitHub Actions. This guide covers workflow syntax, secrets management, matrix builds, Docker publishing, and zero-downtime deployment strategies.",
        """## Introduction

Continuous Integration and Continuous Deployment (CI/CD) is the practice of automatically testing, building, and deploying code every time a change is pushed. Before CI/CD, deployments were manual, infrequent, and stressful. With it, teams can deploy dozens of times per day with confidence. GitHub Actions has democratized this — it's built into GitHub, free for public repos, and powerful enough for enterprise workflows.

## Core Concepts

**Workflow**: A YAML file in `.github/workflows/` that defines an automated process.
**Job**: A set of steps that run on the same runner (virtual machine).
**Step**: A single task — running a command or calling an Action.
**Action**: A reusable, packaged workflow step (from the marketplace or your own repo).
**Runner**: The VM that executes jobs. GitHub provides Ubuntu, Windows, and macOS.
**Trigger (on)**: Events that start the workflow — push, pull_request, schedule, workflow_dispatch.

## A Basic CI Pipeline

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/testdb
        run: pytest tests/ -v --tb=short --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

## Secrets Management

Never hardcode credentials. Store them in GitHub repository secrets (Settings → Secrets → Actions):

```yaml
- name: Deploy
  env:
    SSH_KEY: ${{ secrets.VPS_SSH_KEY }}
    DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
  run: ./scripts/deploy.sh
```

For organization-wide secrets, use GitHub Environments — each environment (staging, production) has its own set of secrets and can require manual approval before deployment.

## Matrix Builds

Test across multiple Python/Node versions simultaneously:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
    os: [ubuntu-latest, macos-latest]

runs-on: ${{ matrix.os }}

steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

This runs 6 parallel jobs (3 Python versions × 2 OSes), catching environment-specific bugs early.

## Docker Build and Push

```yaml
  build-and-push:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/backend:latest
            ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

The `cache-from/cache-to: type=gha` uses GitHub Actions cache for Docker layer caching, drastically reducing build times on subsequent runs.

## Zero-Downtime Deployment via SSH

```yaml
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: deploy
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /app
            docker compose pull
            docker compose up -d --no-deps --scale backend=2 backend
            sleep 10
            docker compose up -d --no-deps --scale backend=1 backend
            docker image prune -f
```

The `--no-deps` flag updates only the backend service without restarting the database.

## Scheduled Workflows

```yaml
on:
  schedule:
    - cron: "0 2 * * *"  # Every day at 2 AM UTC
```

Use cases: database backups, nightly security scans, dependency updates, analytics reports.

## Reusable Workflows

Extract common workflows to avoid duplication:

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      python-version:
        type: string
        default: "3.12"

# .github/workflows/ci.yml
jobs:
  test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: "3.11"
```

## Caching Dependencies

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

Cache keys based on lock file hashes ensure caches are invalidated when dependencies change.

## Deployment Protection Rules

For production deployments, add a required reviewer in GitHub Environments. The workflow will pause and send a notification to the reviewer before proceeding. This is your last line of defense against accidental production deployments.

## Conclusion

GitHub Actions has made professional CI/CD accessible to every project, not just those with dedicated DevOps teams. Start with a basic test pipeline, add Docker builds when you containerize, then graduate to environment-based deployments with manual approvals for production. Each step of automation reduces the risk and friction of shipping software.
""",
        16,
        False,
        ["DevOps", "Web Development"],
    ),
    # 12 -----------------------------------------------------------------------
    (
        "Vector Databases Explained: How Semantic Search Powers Modern AI Applications",
        "vector-databases-semantic-search-ai-applications",
        "Vector databases are the memory layer of modern AI applications. Learn how embeddings, similarity search, and ANN algorithms like HNSW work, and how to choose and use the right vector store for your use case.",
        """## Introduction

When you ask ChatGPT a question about your uploaded PDF, or when Spotify recommends a song that sounds like your favorites, or when Google returns a relevant result even when you phrased your query differently than any document uses — these are all powered by the same underlying technology: **vector embeddings** and **semantic search**. Vector databases are the infrastructure that makes these experiences possible at scale.

## What is an Embedding?

An embedding is a dense numerical representation of data — text, images, audio, or code — in a high-dimensional vector space. The key property is that semantically similar items have similar vectors (small geometric distance).

```
"The cat sat on the mat"    → [0.21, -0.15, 0.87, ..., 0.03]  (1536 dimensions)
"A feline rested on a rug"  → [0.22, -0.14, 0.85, ..., 0.04]  (very similar!)
"PostgreSQL is a database"  → [-0.83, 0.67, -0.21, ..., 0.91] (very different!)
```

This means we can answer the question "which of these documents is most relevant to this query?" as a geometric problem: find the vector closest to the query vector.

## How Vector Search Works

### Brute-Force (Exact Search)

For small datasets, compute the dot product or cosine similarity between the query vector and every stored vector:

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def exact_search(query: np.ndarray, vectors: list[np.ndarray], k: int) -> list[int]:
    similarities = [cosine_similarity(query, v) for v in vectors]
    return sorted(range(len(vectors)), key=lambda i: similarities[i], reverse=True)[:k]
```

This is O(n) per query. At millions of vectors, it becomes too slow.

### Approximate Nearest Neighbor (ANN)

For large datasets, ANN algorithms trade a small amount of accuracy for massive speed gains.

**HNSW (Hierarchical Navigable Small World)** is the dominant ANN algorithm. It builds a multi-layer graph where each node connects to nearby neighbors. Search starts at the top (sparse) layer and "drills down" to find approximate nearest neighbors.

- O(log n) query time
- O(n log n) build time
- Excellent recall (>99%) with good parameters
- Used by: pgvector, Qdrant, Weaviate, Pinecone

**IVF (Inverted File Index)**: Clusters vectors into buckets. At query time, only searches the most relevant clusters. Faster to build, slightly lower recall than HNSW.

## Distance Metrics

| Metric | Formula | Best For |
|--------|---------|----------|
| Cosine Similarity | dot(a,b) / (|a| * |b|) | Text (normalized) |
| Euclidean (L2) | sqrt(sum((a-b)²)) | Image features |
| Dot Product | sum(a*b) | When vectors are pre-normalized |
| Hamming | count(a XOR b) | Binary embeddings |

For text embeddings from OpenAI, cosine similarity is standard. For image and multimodal embeddings, L2 is common.

## Vector Databases Compared

### pgvector (PostgreSQL Extension)

Best when you're already on Postgres and don't need massive scale:

```sql
CREATE EXTENSION vector;

CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(1536)
);

CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Semantic search query
SELECT content, 1 - (embedding <=> $1::vector) AS similarity
FROM documents
ORDER BY embedding <=> $1::vector
LIMIT 5;
```

### Qdrant

Rust-based, fast, rich payload filtering:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=embedding,
            payload={"text": "...", "source": "handbook.pdf", "department": "hr"},
        )
    ],
)

# Filtered semantic search
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter={"must": [{"key": "department", "match": {"value": "hr"}}]},
    limit=5,
)
```

Payload filtering happens before ANN search, narrowing the search space efficiently.

### Pinecone

Managed, serverless, no infrastructure to run. Best for teams that want to focus on the application layer:

```python
from pinecone import Pinecone

pc = Pinecone(api_key="your-key")
index = pc.Index("my-index")

index.upsert(vectors=[
    {"id": "doc-1", "values": embedding, "metadata": {"source": "faq.pdf"}}
])

results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
```

## Multi-Vector Search

Modern retrieval often goes beyond a single query vector:

- **ColBERT**: Stores one embedding per token, enables more precise matching at higher storage cost.
- **Multi-vector documents**: Store separate embeddings for title, abstract, and body; search all three.
- **Parent-child retrieval**: Store small chunk embeddings for precision; retrieve the full parent section for context.

## Production Considerations

- **Index warmup**: HNSW indexes must be loaded into memory for fast search. Cold starts on large indexes take time.
- **Embedding model consistency**: If you change embedding models, you must re-embed everything. Treat the model as a versioned dependency.
- **Dimension mismatch**: Collection dimension is fixed at creation time. Store dimension in your config.
- **Scalability**: Most vector DBs shard horizontally. Plan your shard key (namespace, tenant ID) early.
- **Backup**: Vector indexes are expensive to rebuild. Back up both the raw vectors and metadata.

## Conclusion

Vector databases are the memory layer of modern AI applications. Understanding how embeddings encode meaning, how ANN algorithms efficiently search high-dimensional spaces, and the tradeoffs between different vector stores gives you the tools to build the recommendation systems, semantic search engines, and RAG pipelines that define the current generation of AI products.
""",
        18,
        False,
        ["Artificial Intelligence", "Machine Learning", "New Tech"],
    ),
    # 13 -----------------------------------------------------------------------
    (
        "WebSockets vs Server-Sent Events vs Long Polling: Choosing Real-Time Technology",
        "websockets-sse-long-polling-realtime-technology",
        "Compare the three main approaches to real-time web communication — WebSockets, SSE, and long polling — with implementation examples, use cases, and guidance on when to choose each.",
        """## Introduction

Modern web applications demand real-time capabilities: live chat, notifications, collaborative editing, live sports scores, stock tickers, and AI response streaming. HTTP's request-response model was designed for document retrieval, not bidirectional live data. Three main approaches have emerged to bridge this gap: long polling, Server-Sent Events (SSE), and WebSockets. Each has distinct tradeoffs that make it the right choice for different use cases.

## Long Polling

Long polling is the simplest approach and works over standard HTTP. The client makes a request, the server holds it open until data is available (or a timeout occurs), responds, and the client immediately sends another request.

### How It Works

```
Client → GET /events (held open)
Server: (waiting for new data...)
Server: (new data available!) → 200 OK { data: "..." }
Client → GET /events (immediately re-opens)
```

### Implementation

```python
# FastAPI long polling endpoint
@router.get("/poll")
async def long_poll(last_id: int = 0, timeout: int = 30):
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        events = await db.get_events_since(last_id)
        if events:
            return {"events": events}
        await asyncio.sleep(0.5)
    return {"events": []}
```

```javascript
// Client
async function poll(lastId = 0) {
  const res = await fetch(`/poll?last_id=${lastId}`);
  const { events } = await res.json();
  if (events.length > 0) {
    processEvents(events);
    lastId = events[events.length - 1].id;
  }
  poll(lastId); // immediately re-poll
}
```

### Pros and Cons

**Pros:**
- Works everywhere — proxies, CDNs, load balancers all understand HTTP.
- Simple to implement with any HTTP framework.
- Firewall-friendly.

**Cons:**
- High server connection overhead (each poll holds a connection open).
- Latency proportional to poll interval.
- Not suitable for very high-frequency updates.

**Best for:** Simple notification systems, admin dashboards, low-frequency updates where you want maximum compatibility.

---

## Server-Sent Events (SSE)

SSE is a W3C standard for one-directional streaming from server to client over a persistent HTTP connection. The server pushes updates as they happen; the client listens.

### How It Works

The server sends a response with `Content-Type: text/event-stream` and writes newline-delimited events indefinitely. The client's EventSource API automatically handles reconnection.

### Server Implementation (FastAPI)

```python
from fastapi.responses import StreamingResponse
import asyncio

async def event_generator(client_id: str):
    while True:
        # Wait for new data (pub/sub, queue, etc.)
        data = await redis_pubsub.get_message(client_id)
        if data:
            yield f"data: {json.dumps(data)}\\n\\n"
        await asyncio.sleep(0.1)

@router.get("/stream")
async def stream(request: Request):
    async def generate():
        async for chunk in event_generator(request.headers.get("X-Client-ID")):
            if await request.is_disconnected():
                break
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

### Client Implementation

```javascript
const source = new EventSource('/stream');

source.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateUI(data);
};

source.onerror = () => {
  console.log('Reconnecting...');
  // EventSource automatically reconnects with exponential backoff
};

// Named events
source.addEventListener('notification', (event) => {
  showNotification(JSON.parse(event.data));
});
```

### SSE Event Format

```
data: {"message": "Hello"}

event: notification
data: {"type": "info", "text": "New comment"}
id: 42

: this is a comment (ignored by client)
```

The `id` field enables the browser to send `Last-Event-ID` on reconnect, so you don't miss events.

### SSE and AI Streaming

SSE is the standard for streaming LLM responses:

```python
async def stream_ai_response(prompt: str):
    async for chunk in openai_client.chat.completions.stream(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    ):
        if chunk.choices[0].delta.content:
            yield f"data: {json.dumps({'text': chunk.choices[0].delta.content})}\\n\\n"
    yield "data: [DONE]\\n\\n"
```

**Pros:**
- Simple — works over standard HTTP/2.
- Native browser support via EventSource API.
- Automatic reconnection built in.
- Works through most proxies and CDNs.

**Cons:**
- One-directional only (server → client).
- Limited to 6 concurrent SSE connections per domain in HTTP/1.1 (not an issue with HTTP/2).
- No binary data support (must base64 encode).

**Best for:** AI response streaming, notifications, live feeds, dashboards, any server-to-client push.

---

## WebSockets

WebSockets provide a full-duplex, persistent, low-overhead connection. After an initial HTTP handshake, the connection upgrades to the WebSocket protocol — a framed binary/text protocol with minimal overhead per message.

### How It Works

```
Client → HTTP GET /ws (Upgrade: websocket)
Server → 101 Switching Protocols
[persistent bidirectional connection]
Client ↔ Server: framed messages at will
```

### Server Implementation (FastAPI)

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.connections.setdefault(room, []).append(ws)

    async def broadcast(self, room: str, message: dict):
        for ws in self.connections.get(room, []):
            await ws.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{room}")
async def websocket_endpoint(ws: WebSocket, room: str):
    await manager.connect(room, ws)
    try:
        while True:
            data = await ws.receive_json()
            await manager.broadcast(room, {
                "user": data["user"],
                "message": data["message"],
                "timestamp": datetime.utcnow().isoformat(),
            })
    except WebSocketDisconnect:
        manager.connections[room].remove(ws)
```

### Client Implementation

```javascript
const ws = new WebSocket('wss://example.com/ws/room-1');

ws.onopen = () => {
  ws.send(JSON.stringify({ user: 'Alice', message: 'Hello!' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  appendMessage(data);
};

ws.onerror = (error) => console.error('WebSocket error:', error);
ws.onclose = () => reconnect(); // Implement your own reconnection logic
```

**Pros:**
- Full bidirectional communication.
- Very low per-message overhead (~2-14 bytes).
- Native binary support.
- Ideal for latency-sensitive applications.

**Cons:**
- More complex server state management.
- No built-in reconnection (must implement yourself).
- Some corporate proxies block WebSockets.
- Harder to scale horizontally (sticky sessions or pub/sub backend needed).

**Best for:** Chat, multiplayer games, collaborative editing (Google Docs style), trading platforms, live coding environments.

---

## Decision Matrix

| Requirement | Long Polling | SSE | WebSocket |
|---|---|---|---|
| Server → Client push | OK | Best | Best |
| Client → Server | Request-response | Not supported | Best |
| Bidirectional | No | No | Yes |
| Binary data | No | No (encode) | Yes |
| Auto-reconnect | Manual | Built-in | Manual |
| Proxy compatibility | Excellent | Good | Sometimes issues |
| Horizontal scaling | Easy | Easy | Needs sticky/pubsub |
| Implementation complexity | Low | Low | Medium |

## Conclusion

For AI response streaming, notifications, and server-push scenarios — SSE is the pragmatic choice. For interactive real-time applications (chat, collaboration, gaming) — WebSockets are the right tool. Long polling remains useful as a fallback for environments where SSE/WebSockets are unreliable. All three are production-ready; choose based on communication direction and operational requirements.
""",
        18,
        False,
        ["Web Development", "System Design", "New Tech"],
    ),
    # 14 -----------------------------------------------------------------------
    (
        "Deep Learning Fundamentals: Neural Networks, Backpropagation, and CNNs",
        "deep-learning-fundamentals-neural-networks-backpropagation-cnns",
        "Build intuition for how neural networks actually learn — from perceptrons and activation functions through backpropagation, gradient descent, and convolutional networks for computer vision.",
        """## Introduction

Deep learning is the engine behind voice assistants, image recognition, medical diagnosis, autonomous vehicles, and the large language models transforming software development. Despite its revolutionary impact, the core mathematics is surprisingly accessible — it's calculus, linear algebra, and clever engineering stacked on top of each other. This post builds the intuition from the ground up.

## The Perceptron: The Atom of Neural Networks

A single perceptron computes a weighted sum of inputs and passes it through an activation function:

```
output = activation(w₁x₁ + w₂x₂ + ... + wₙxₙ + bias)
```

Where `w` are weights and `x` are inputs. The perceptron can learn to classify linearly separable data by adjusting weights — but it can't solve XOR (the classic limitation). Stacking perceptrons into layers solves this.

## Activation Functions

Without non-linear activation functions, a multi-layer network collapses to a single linear transformation regardless of depth. Activation functions introduce non-linearity:

### ReLU (Rectified Linear Unit)

```
f(x) = max(0, x)
```

Simple, cheap, and works remarkably well. The dominant activation for hidden layers. The "dying ReLU" problem (neurons that never activate) is addressed by Leaky ReLU or ELU.

### Sigmoid

```
f(x) = 1 / (1 + e^(-x))
```

Outputs 0-1. Used in output layers for binary classification. Suffers from vanishing gradients in deep networks.

### Softmax

```
f(xᵢ) = e^xᵢ / Σⱼ e^xⱼ
```

Converts a vector of scores to a probability distribution summing to 1. Standard for multi-class classification output layers.

## Forward Pass

In a forward pass, data flows from input to output through layers of matrix multiplications and activation functions:

```python
import numpy as np

def forward(X, weights, biases, activations):
    a = X
    cache = []
    for W, b, activation in zip(weights, biases, activations):
        z = a @ W + b          # Linear transformation
        a = activation(z)      # Non-linear activation
        cache.append((a, z))
    return a, cache
```

## Loss Functions

The loss function measures how wrong the model's predictions are. The goal of training is to minimize it.

**Mean Squared Error** (regression):
```
L = (1/n) Σ (ŷᵢ - yᵢ)²
```

**Cross-Entropy Loss** (classification):
```
L = -(1/n) Σ yᵢ log(ŷᵢ)
```

Cross-entropy heavily penalizes confident wrong predictions, which is exactly what you want when training classifiers.

## Backpropagation: How Networks Learn

Backpropagation is the algorithm that computes gradients of the loss with respect to every weight in the network. It's an application of the **chain rule** of calculus.

If the loss L depends on weight W through intermediate computations:

```
∂L/∂W = (∂L/∂a) × (∂a/∂z) × (∂z/∂W)
```

This chain of derivatives is computed backward from the output layer to the input layer — hence "backpropagation."

```python
def backward(loss_grad, cache, weights):
    grads = []
    da = loss_grad
    for (a, z), W in zip(reversed(cache), reversed(weights)):
        dz = da * relu_derivative(z)    # Chain rule through activation
        dW = prev_a.T @ dz              # Gradient w.r.t. weights
        db = dz.sum(axis=0)             # Gradient w.r.t. bias
        da = dz @ W.T                   # Gradient to pass to previous layer
        grads.append((dW, db))
    return grads
```

## Gradient Descent and Optimizers

Once we have gradients, we update weights to reduce the loss:

**Stochastic Gradient Descent (SGD):**
```
W = W - learning_rate × ∂L/∂W
```

Modern training uses mini-batches (SGD over small random subsets) and sophisticated optimizers:

**Adam (Adaptive Moment Estimation)** — the default optimizer for most tasks:

```python
# Adam update rule (simplified)
m = beta1 * m + (1 - beta1) * grad        # First moment (momentum)
v = beta2 * v + (1 - beta2) * grad**2     # Second moment (adaptive LR)
m_hat = m / (1 - beta1**t)               # Bias correction
v_hat = v / (1 - beta2**t)
W = W - lr * m_hat / (sqrt(v_hat) + eps)
```

Adam adapts the learning rate per parameter — parameters with large, consistent gradients get smaller updates; parameters with small or noisy gradients get larger ones.

## Regularization: Preventing Overfitting

### Dropout

Randomly zero out neurons during training, forcing the network to learn redundant representations:

```python
def dropout(x, rate=0.5, training=True):
    if not training:
        return x
    mask = np.random.binomial(1, 1 - rate, x.shape) / (1 - rate)
    return x * mask
```

### Batch Normalization

Normalizes layer inputs to have zero mean and unit variance, allowing higher learning rates and reducing sensitivity to initialization:

```
x_norm = (x - μ_batch) / sqrt(σ²_batch + ε)
y = γ × x_norm + β   # Learned scale and shift
```

## Convolutional Neural Networks (CNNs)

Fully connected networks treat each pixel independently — a 224×224 image has 150,528 inputs. CNNs exploit spatial structure through **convolutions**:

A convolution applies a small filter (e.g., 3×3) across the image, computing a dot product at each position. The filter learns to detect features — edges, textures, shapes — regardless of where they appear in the image (translation invariance).

```python
import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 32 filters, 3×3
            nn.ReLU(),
            nn.MaxPool2d(2),                              # Downsample 2×
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)
```

### Key CNN Operations

- **Convolution**: Feature detection with shared weights across spatial positions.
- **Pooling**: Downsampling (MaxPool takes the maximum in each window) — reduces spatial size and adds position invariance.
- **Batch Norm**: Stabilizes training in deep networks.
- **Skip Connections (ResNet)**: Add the input directly to the output of a block — allows training networks 100+ layers deep by preventing vanishing gradients.

## Transfer Learning

Training CNNs from scratch requires millions of labeled images. Transfer learning uses weights pre-trained on ImageNet and fine-tunes them for your task:

```python
import torchvision.models as models

model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# Freeze feature extraction layers
for param in model.parameters():
    param.requires_grad = False

# Replace classification head
model.fc = nn.Linear(2048, num_classes)

# Only train the new head
optimizer = torch.optim.Adam(model.fc.parameters(), lr=1e-3)
```

This works because early CNN layers learn universal features (edges, textures) that transfer across tasks. Only the later, task-specific layers need retraining.

## Conclusion

Neural networks are, at their core, function approximators trained with gradient descent. The magic is not in any individual component — it's in the combination of depth, non-linearity, large datasets, and the backpropagation algorithm that efficiently computes gradients through arbitrary computational graphs. Building this intuition makes every neural network paper, library, and debugging session more tractable.
""",
        21,
        False,
        ["Machine Learning", "Artificial Intelligence", "Python"],
    ),
    # 15 -----------------------------------------------------------------------
    (
        "The State of AI in 2025: Agents, Multimodality, and What Comes Next",
        "state-of-ai-2025-agents-multimodality-future",
        "A comprehensive review of where AI stands in 2025 — the rise of autonomous AI agents, multimodal foundation models, open-source progress, regulatory landscape, and the technical frontiers researchers are actively pushing.",
        """## Introduction

2025 is arguably the most consequential year in the history of artificial intelligence. The pace of progress has not slowed — if anything, it has accelerated. Foundation models have grown more capable, more efficient, and more multimodal. AI agents are moving from demos to production deployments. Open-source models have narrowed the gap with proprietary frontier labs. Regulators are scrambling to keep up. This post takes a clear-eyed look at the state of the field.

## The Rise of AI Agents

The most significant shift of 2024-2025 has been from **chatbots** to **agents**. A chatbot responds to a single prompt. An agent perceives its environment, maintains state, uses tools, and takes sequences of actions to accomplish a goal.

### What Makes an Agent

An agent architecture typically includes:

1. **LLM backbone**: Reasoning and planning engine.
2. **Tools**: Functions the model can call — web search, code execution, database queries, API calls.
3. **Memory**: Short-term (context window), long-term (vector store), and episodic (conversation history).
4. **Orchestration loop**: The cycle of observe → reason → act → observe.

```python
# Simplified ReAct agent loop
def run_agent(user_query: str, tools: dict, max_steps: int = 10):
    messages = [{"role": "user", "content": user_query}]

    for step in range(max_steps):
        response = llm.chat(messages, tools=tools)

        if response.finish_reason == "stop":
            return response.content  # Final answer

        # Model wants to call a tool
        tool_call = response.tool_calls[0]
        tool_result = tools[tool_call.name](**tool_call.arguments)

        messages.append({"role": "assistant", "tool_calls": [tool_call]})
        messages.append({"role": "tool", "content": str(tool_result)})
```

### Multi-Agent Systems

Single agents are powerful; networks of specialized agents are more powerful. Frameworks like **LangGraph**, **AutoGen**, **CrewAI**, and **Claude's agent SDK** enable multi-agent architectures where agents delegate subtasks to other agents, parallelize work, and cross-check each other's outputs.

A software engineering agent might orchestrate: a coder agent, a code reviewer agent, a test runner agent, and a documentation agent — each specialized, coordinated by an orchestrator.

### Production Agent Challenges

Agents are powerful but introduce new failure modes:
- **Irreversible actions**: An agent that sends emails or deploys code can cause real damage from a planning error.
- **Compounding errors**: Mistakes in early steps propagate and amplify.
- **Tool reliability**: Agents depend on external APIs that fail, throttle, or return unexpected results.
- **Context management**: Long agent runs exceed context windows.
- **Prompt injection**: Malicious content in retrieved data can hijack agent behavior.

The field is actively developing patterns for agent reliability: checkpointing, human-in-the-loop confirmations for high-stakes actions, and sandboxed execution environments.

## Multimodal Foundation Models

The dominant trend in foundation models is the collapse of modality boundaries. Models no longer specialize in text or images or audio — they handle all of them within a unified architecture.

**GPT-4o** ("omni") processes text, images, and audio natively and can respond in any combination. **Gemini 1.5/2.0** integrates text, images, video, and code with a 2M-token context window. **Claude 3.5** demonstrates strong reasoning over text and images.

### What Multimodality Enables

- **Document understanding**: Parse PDFs, invoices, forms with complex layouts — beyond OCR.
- **Visual reasoning**: "What's wrong with this circuit diagram?" or "Describe the bug visible in this screenshot."
- **Video analysis**: Summarize an hour-long meeting recording, identify key moments.
- **Real-time audio**: Conversational AI with natural prosody and turn-taking.

### Upcoming Modalities

The frontier models are adding: video generation (Sora), 3D scene understanding, real-time sensing from wearables and robots, and protein structure prediction (AlphaFold 3 for drug discovery).

## Open-Source Catches Up

The proprietary/open-source capability gap has narrowed dramatically. Key milestones:

- **Meta's LLaMA 3** (70B, 405B): Competitive with GPT-3.5 and approaches GPT-4 on many benchmarks.
- **Mistral**: Efficient, fast, deployable on consumer hardware.
- **Qwen 2.5** (Alibaba): Strong multilingual capabilities, competitive on coding.
- **DeepSeek R1**: Chinese frontier model matching GPT-4 reasoning at a fraction of the compute cost — a significant signal about efficiency improvements.

The implication: organizations with data privacy requirements or deployment constraints can now run competitive models on their own infrastructure.

## Reasoning Models

2024-2025 saw the emergence of "reasoning models" — models trained to spend more compute at inference time rather than just answering immediately.

OpenAI's o1/o3, Anthropic's Claude 3.7 Sonnet, and Google's Gemini Thinking all exhibit extended internal reasoning before responding. On complex math, science, and coding benchmarks, these models dramatically outperform their instant-response counterparts.

The tradeoff: latency (seconds to minutes for hard problems) and cost (more tokens generated). But for tasks where correctness matters more than speed — debugging, mathematical proofs, complex planning — reasoning models represent a qualitative capability jump.

## Efficiency: Smaller, Faster, Cheaper

While frontier models grow larger, the field is equally focused on efficiency:

**Quantization**: Reducing weight precision from 32-bit to 4-bit or even 1-bit with minimal quality loss. **llama.cpp** and **GGUF** formats enable running 7B parameter models on laptops.

**Speculative Decoding**: A small draft model proposes tokens; the large model verifies them in parallel. 2-4x speedup with identical output quality.

**Mixture of Experts (MoE)**: Route each token to a subset of model parameters rather than activating all of them. GPT-4 and Mixtral use this architecture — large total parameters, smaller active parameters per token, lower inference cost.

**Distillation**: Train smaller models to mimic larger ones. GPT-4 capabilities in a model 10x smaller.

## The Regulatory Landscape

**EU AI Act** (effective August 2024): Tiered risk-based regulation. High-risk applications (medical, justice, critical infrastructure) face strict requirements for transparency, human oversight, and conformity assessment. General-purpose AI models above a compute threshold must publish technical documentation and comply with copyright law.

**US Executive Orders and NIST**: The US has taken a lighter touch — voluntary commitments from major AI labs, NIST's AI Risk Management Framework, and export controls on advanced chips.

**China**: Strict regulation on generative AI content, mandatory registration of AI systems, and significant state investment in domestic AI development.

## What Comes Next

**Short term (1-2 years):**
- Agents go mainstream in enterprise software (coding, customer support, research)
- Video generation becomes commodity infrastructure
- On-device AI becomes powerful enough for most everyday tasks
- AI-native developer tooling replaces traditional IDEs for many workflows

**Medium term (3-5 years):**
- Autonomous research agents that propose and test hypotheses
- AI-designed materials, drugs, and proteins reaching clinical/production stages
- Significant workforce disruption in knowledge work sectors
- Competing national AI ecosystems with different regulatory frameworks

**Open questions the field hasn't answered:**
- Can current architectures scale to human-level general reasoning, or is a new paradigm needed?
- Will alignment techniques scale with model capabilities?
- How do we build AI systems that are robustly reliable rather than impressively capable but brittle?

## Conclusion

AI in 2025 is defined by agents, multimodality, and the tension between unprecedented capability and unresolved reliability challenges. The technology has moved faster than governance, faster than tooling, and faster than most organizations' ability to integrate it effectively. The developers who understand both the capabilities and the limitations — who can build responsibly on this foundation — will define what the next decade of software looks like.
""",
        22,
        True,
        ["Artificial Intelligence", "Machine Learning", "New Tech"],
    ),
]


async def main():
    await init_db()

    async with AsyncSessionLocal() as db:

        # Ensure all tags exist
        tag_map: dict[str, Tag] = {}
        for name, slug in TAG_DEFS:
            result = await db.execute(select(Tag).where(Tag.slug == slug))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=name, slug=slug)
                db.add(tag)
                await db.flush()
                print(f"  Created tag: {name}")
            tag_map[name] = tag

        await db.flush()

        # Insert blog posts
        for title, slug, excerpt, content, reading_time, featured, tag_names in POSTS:
            result = await db.execute(select(BlogPost).where(BlogPost.slug == slug))
            if result.scalar_one_or_none():
                print(f"⚠️  Skipping (already exists): {title}")
                continue

            post = BlogPost(
                title=title,
                slug=slug,
                excerpt=excerpt,
                content=content,
                reading_time_minutes=reading_time,
                is_published=True,
                featured=featured,
            )
            post.tags = [tag_map[t] for t in tag_names if t in tag_map]
            db.add(post)
            print(f"✅ Added: {title}")

        await db.commit()
        print("\nDone. All 15 blog posts added.")


if __name__ == "__main__":
    asyncio.run(main())
