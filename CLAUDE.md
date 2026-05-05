# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack portfolio web application with AI chatbot. Backend: FastAPI + PostgreSQL + Redis + Celery. Frontend: React 18 + TypeScript + Vite + Tailwind CSS. Deployed via Docker Compose behind Nginx.

## Development Commands

### Local Development
```bash
# Start all services (backend port 8000, frontend port 3000)
docker-compose up

# API docs available at http://localhost:8000/api/docs
```

### Frontend (`frontend/`)
```bash
npm run dev        # Vite dev server on port 3000
npm run build      # TypeScript compile + Vite build
npm run lint       # ESLint on .ts/.tsx files
npm run typecheck  # tsc --noEmit type checking
npm run preview    # Preview production build
```

### Backend (`backend/`)
```bash
# Run tests
pip install pytest pytest-asyncio httpx
pytest tests/ -v --tb=short

# Database migrations
alembic upgrade head      # Apply migrations
alembic revision --autogenerate -m "description"  # Create new migration
```

## Architecture

### Backend (`backend/app/`)
- **`main.py`** — FastAPI app entry, mounts all routers, configures CORS
- **`core/config.py`** — Pydantic settings loaded from `.env`
- **`core/database.py`** — Async SQLAlchemy + asyncpg setup
- **`core/security.py`** — JWT creation/verification, password hashing
- **`api/v1/endpoints/`** — 8 route modules: `auth`, `blog`, `projects`, `chat`, `contact`, `github`, `analytics`, `resume`
- **`models/`** — SQLAlchemy ORM models (Admin, BlogPost, Tag, Project, ContactMessage, PageView, VisitorSession)
- **`schemas/`** — Pydantic request/response models
- **`services/`** — Business logic: `ai_service.py` (OpenAI streaming with Redis session memory), `github_service.py`, `email_service.py`, `analytics_service.py`
- **`tasks/`** — Celery worker and GitHub sync background jobs
- **`alembic/`** — Database migration scripts

### Frontend (`frontend/src/`)
- **`App.tsx`** — React Router v6 route definitions
- **`pages/`** — Route components (Home, Blog, BlogPost, Projects, ProjectDetail, Resume, Contact)
- **`components/chatbot/`** — Streaming AI chatbot component
- **`components/layout/`** — Navbar, Footer
- **`api/`** — Axios client configured to proxy to `/api` (backend)
- **`store/themeStore.ts`** — Zustand dark/light mode state
- **`types/`** — Shared TypeScript interfaces

### Data Flow
- Frontend uses React Query (5min stale time) for server state; Zustand only for theme
- Chatbot streams from `/api/v1/chat` via SSE
- Celery worker syncs GitHub repos periodically (Redis as broker)
- All admin endpoints require JWT Bearer token from `/api/v1/auth/login`

### Infrastructure
- `docker-compose.yml` — 5 services: `db` (Postgres 16), `redis`, `backend`, `celery`, `frontend`
- `docker-compose.prod.yml` — Production stack; backend runs `alembic upgrade head` on startup, then uvicorn with 2 workers
- `nginx/nginx.conf` — Reverse proxy: `/api/*` → backend:8000, all else → frontend:80

## Environment Setup

Copy `.env.example` to `.env`. Key variables:
- `DATABASE_URL`, `REDIS_URL` — service connections
- `SECRET_KEY` — JWT signing
- `OPENAI_API_KEY` — chatbot
- `GITHUB_TOKEN` — repo sync
- `AWS_*` — S3 for resume PDF
- `MAIL_*` — SMTP for contact form
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` — initial admin account

## CI/CD

`.github/workflows/deploy.yml` runs on push to `main`:
1. `test-backend` — pytest against real Postgres + Redis services
2. `test-frontend` — TypeScript check + ESLint
3. `build-and-push` — Docker images to GHCR
4. `deploy` — SSH to VPS, pull images, `docker-compose -f docker-compose.prod.yml up -d`