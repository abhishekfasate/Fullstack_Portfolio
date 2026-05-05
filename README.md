# Portfolio Full-Stack Application

A personal portfolio web app with an AI-powered chatbot. Built with FastAPI (backend) and React + TypeScript (frontend), deployed via Docker Compose behind Nginx.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | FastAPI 0.111 + Python 3.11 | REST API |
| Database | PostgreSQL 16 + SQLAlchemy 2 | Persistent storage |
| Async DB driver | asyncpg | Non-blocking DB queries |
| Migrations | Alembic | DB schema versioning |
| Auth | JWT (python-jose) + bcrypt | Admin login |
| Cache / Queue | Redis | Chat history + Celery broker |
| Background tasks | Celery | GitHub repo sync |
| AI | OpenAI GPT-4o | Chatbot |
| Email | SMTP via `emails` lib | Contact form |
| Storage | AWS S3 (boto3) | Resume PDF |
| Frontend | React 18 + TypeScript + Vite | UI |
| Styling | Tailwind CSS | CSS utility classes |
| Frontend state | React Query + Zustand | Server + client state |
| Proxy | Nginx | Routes /api/* to backend |
| Containerization | Docker + Docker Compose | Dev and prod parity |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app, middleware, startup
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic settings from .env
│   │   │   ├── database.py          # Async SQLAlchemy engine + session
│   │   │   └── security.py          # JWT + bcrypt password utils
│   │   ├── api/v1/
│   │   │   ├── router.py            # Combines all sub-routers under /api/v1
│   │   │   ├── deps.py              # Reusable dependencies (auth guard, DB session)
│   │   │   └── endpoints/
│   │   │       ├── auth.py          # POST /auth/token (admin login)
│   │   │       ├── blog.py          # Blog CRUD
│   │   │       ├── projects.py      # Projects CRUD
│   │   │       ├── chat.py          # AI chatbot (regular + SSE streaming)
│   │   │       ├── contact.py       # Contact form submission
│   │   │       ├── github.py        # GitHub repository data
│   │   │       ├── analytics.py     # Page view tracking
│   │   │       └── resume.py        # Resume PDF download (S3)
│   │   ├── models/                  # SQLAlchemy ORM table definitions
│   │   ├── schemas/                 # Pydantic request/response models
│   │   ├── services/                # Business logic (AI, GitHub, email, analytics)
│   │   └── tasks/                   # Celery background jobs
│   ├── alembic/                     # Database migration scripts
│   ├── scripts/seed.py              # Seeds initial admin account
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.tsx                  # React Router route definitions
│       ├── pages/                   # Route page components
│       ├── components/
│       │   ├── chatbot/             # Streaming AI chat UI
│       │   └── layout/              # Navbar, Footer
│       ├── api/                     # Axios client (proxies to /api)
│       ├── store/themeStore.ts      # Zustand dark/light mode
│       └── types/                   # Shared TypeScript interfaces
├── nginx/nginx.conf                 # /api/* → backend, all else → frontend
├── docker-compose.yml               # Local development stack
└── docker-compose.prod.yml          # Production stack
```

---

## API Request Flow

```
Client (Browser)
  │
  ▼
Nginx (/api/* → backend:8000)
  │
  ▼
main.py — CORSMiddleware, GZipMiddleware
  │
  ▼
router.py — matches /api/v1/<feature>
  │
  ▼
endpoints/<feature>.py — route function
  │
  ├── deps.py/get_db()           → opens async DB session
  ├── deps.py/get_current_admin() → JWT auth (protected routes only)
  │
  ▼
services/<feature>_service.py   — business logic (AI, email, etc.)
  │
  ▼
PostgreSQL / Redis / OpenAI API
  │
  ▼
schemas/<feature>.py            — serializes response to JSON
  │
  ▼
HTTP Response to client
```

---

## How to Run

### Prerequisites
- Docker and Docker Compose installed

### 1. Configure environment
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and fill in required values (see below)
```

Required `.env` values:
```env
DATABASE_URL=postgresql+asyncpg://portfolio:portfolio@db:5432/portfolio_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-random-secret-key-here
OPENAI_API_KEY=sk-...
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your-admin-password
```

### 2. Start all services
```bash
docker-compose up
```

This starts 5 containers:
- `db` — PostgreSQL 16 on port 5432
- `redis` — Redis on port 6379
- `backend` — FastAPI on port 8000
- `celery` — Background worker
- `frontend` — React dev server on port 3000

### 3. Seed the admin account
```bash
docker-compose exec backend python scripts/seed.py
```

### 4. Access the app
| URL | Description |
|---|---|
| http://localhost:3000 | React frontend |
| http://localhost:8000/api/docs | Interactive API docs (Swagger UI) |
| http://localhost:8000/health | Health check |

---

## Example API Requests & Responses

### Login (get JWT token)
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -d "username=admin@example.com&password=your-password" \
  -H "Content-Type: application/x-www-form-urlencoded"
```
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### List blog posts
```bash
curl http://localhost:8000/api/v1/blog?limit=5&featured=true
```
```json
[
  {
    "id": 1,
    "title": "Getting Started with FastAPI",
    "slug": "getting-started-with-fastapi",
    "excerpt": "A beginner-friendly intro...",
    "cover_image_url": "https://...",
    "reading_time_minutes": 5,
    "views": 42,
    "tags": [{"id": 1, "name": "Python", "slug": "python"}],
    "featured": true,
    "created_at": "2026-03-25T18:14:00Z"
  }
]
```

### Get a single blog post
```bash
curl http://localhost:8000/api/v1/blog/getting-started-with-fastapi
```

### Create a blog post (requires JWT)
```bash
curl -X POST http://localhost:8000/api/v1/blog \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "excerpt": "Short summary...",
    "content": "## Hello\n\nMarkdown content here.",
    "is_published": true,
    "tag_ids": [1, 2]
  }'
```
```json
{
  "id": 2,
  "title": "My New Post",
  "slug": "my-new-post",
  "excerpt": "Short summary...",
  "content": "## Hello\n\nMarkdown content here.",
  "views": 0,
  "tags": [...],
  "created_at": "2026-03-26T10:00:00Z",
  "updated_at": "2026-03-26T10:00:00Z"
}
```

### Chat with AI
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your projects", "session_id": null}'
```
```json
{
  "reply": "I have worked on several interesting projects...",
  "session_id": "a1b2c3d4-..."
}
```

### Streaming chat (SSE)
```bash
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about yourself"}' \
  --no-buffer
```
```
data: I
data: 'm
data:  a
data:  software
...
event: done
data: a1b2c3d4-...
```

---

## Database Migrations

```bash
# Apply all pending migrations
docker-compose exec backend alembic upgrade head

# Create a new migration after changing a model
docker-compose exec backend alembic revision --autogenerate -m "add cover image to project"
```

---

## Running Tests

```bash
docker-compose exec backend pytest tests/ -v --tb=short
```

---

## Production Deployment

```bash
# Uses docker-compose.prod.yml
# Runs alembic upgrade head on startup, then uvicorn with 2 workers
docker-compose -f docker-compose.prod.yml up -d
```

CI/CD (`.github/workflows/deploy.yml`) runs on push to `main`:
1. Run backend tests (pytest against real Postgres + Redis)
2. Run frontend checks (TypeScript + ESLint)
3. Build and push Docker images to GHCR
4. SSH to VPS and pull + restart containers