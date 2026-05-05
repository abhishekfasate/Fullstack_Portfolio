# Free Deployment Guide

Deploy this portfolio app for free using:
- **GitHub** — source of truth
- **Vercel** — frontend
- **Render** — backend + Celery worker
- **Neon** — PostgreSQL
- **Upstash** — Redis

---

## Prerequisites

- [Git](https://git-scm.com/) installed locally
- Node.js 18+ (for frontend local checks)
- Python 3.11+ (for DB export)
- Docker running locally (to export current data)
- Accounts on: GitHub, Vercel, Render, Neon, Upstash (all free)

---

## Step 0 — Export your current database

Before touching anything else, export the live data from your local Docker Postgres.

```bash
# Make sure your local docker-compose is running
cd /root/ppf
docker-compose up -d db

# Wait a few seconds for DB to be healthy, then dump
docker-compose exec db pg_dump \
  -U portfolio \
  -d portfolio_db \
  --no-owner \
  --no-acl \
  -F p \
  -f /tmp/portfolio_dump.sql

# Copy the dump out of the container
docker cp $(docker-compose ps -q db):/tmp/portfolio_dump.sql ./portfolio_dump.sql
```

You now have `portfolio_dump.sql` in your project root. **Do not commit this file** — it contains your data.

---

## Step 1 — Push to GitHub

### 1.1 — Update .gitignore

Make sure these are in your `.gitignore` (check it exists at root):

```
.env
portfolio_dump.sql
__pycache__/
*.pyc
node_modules/
dist/
.venv/
```

### 1.2 — Create the GitHub repo

1. Go to [github.com/new](https://github.com/new)
2. Name it (e.g. `portfolio`)
3. Set to **Private** (recommended — keeps your config files hidden)
4. Do NOT initialize with README (you already have one)
5. Click **Create repository**

### 1.3 — Push your code

```bash
cd /root/ppf
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
git push -u origin main
```

Verify: your code should appear on GitHub. Confirm `portfolio_dump.sql` and `.env` are NOT listed.

---

## Step 2 — Create Neon PostgreSQL

1. Go to [neon.tech](https://neon.tech) → Sign up free
2. Create a new **Project** (name it `portfolio`)
3. Choose region closest to you
4. Once created, go to **Connection Details**
5. Select **Connection string** → copy the string that looks like:
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
6. Convert it for asyncpg (replace `postgresql://` with `postgresql+asyncpg://`):
   ```
   postgresql+asyncpg://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?ssl=require
   ```

Save both versions — you'll need them:
- **asyncpg version** → `DATABASE_URL` env var for the backend
- **plain psql version** → for importing your dump in Step 2.1

### 2.1 — Import your data into Neon

Neon supports direct `psql` imports. Run this from your local machine:

```bash
# Install psql if you don't have it
# Ubuntu: sudo apt install postgresql-client
# Mac: brew install libpq

psql "postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require" \
  -f portfolio_dump.sql
```

Verify it worked — in the Neon dashboard go to **Tables** and confirm your tables exist (admin, blog_posts, projects, etc.).

---

## Step 3 — Create Upstash Redis

1. Go to [upstash.com](https://upstash.com) → Sign up free
2. Create a **Redis database**
3. Choose region closest to you
4. Once created, go to the database page
5. Copy the **Redis URL** (starts with `rediss://`):
   ```
   rediss://default:password@xxx.upstash.io:6379
   ```

You'll use this same URL for all three Redis vars:
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

---

## Step 4 — Deploy Backend on Render

### 4.1 — Create the Web Service

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click **New** → **Web Service**
3. Connect your `portfolio` GitHub repo
4. Configure:
   - **Name:** `portfolio-backend`
   - **Region:** Same as your Neon/Upstash region
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
5. Choose **Free** plan

### 4.2 — Set environment variables on Render

In the **Environment** tab, add these key-value pairs:

| Key | Value |
|-----|-------|
| `APP_ENV` | `production` |
| `SECRET_KEY` | Generate one: `openssl rand -hex 32` |
| `DATABASE_URL` | Your Neon asyncpg URL from Step 2 |
| `REDIS_URL` | Your Upstash Redis URL from Step 3 |
| `CELERY_BROKER_URL` | Same Upstash Redis URL |
| `CELERY_RESULT_BACKEND` | Same Upstash Redis URL |
| `ALLOWED_ORIGINS` | `https://your-app.vercel.app` (update after Step 6) |
| `GITHUB_TOKEN` | Your GitHub personal access token |
| `GITHUB_USERNAME` | Your GitHub username |
| `MAIL_USERNAME` | Your Gmail address |
| `MAIL_PASSWORD` | Your Gmail app password |
| `MAIL_FROM` | Your Gmail address |
| `MAIL_TO` | Where contact form emails go |
| `MAIL_SERVER` | `smtp.gmail.com` |
| `MAIL_PORT` | `587` |
| `ADMIN_EMAIL` | Your admin login email |
| `ADMIN_PASSWORD` | Strong password for admin panel |
| `AWS_ACCESS_KEY_ID` | (optional, for resume S3) |
| `AWS_SECRET_ACCESS_KEY` | (optional, for resume S3) |
| `AWS_S3_BUCKET` | (optional) |
| `AWS_REGION` | (optional) |

> **Gmail app password:** In Gmail → Account → Security → 2-Step Verification → App passwords → create one for "Mail".

6. Click **Create Web Service**
7. Wait for deploy — first build takes ~3-5 minutes
8. Once deployed, test: `https://portfolio-backend.onrender.com/health` should return `{"status":"ok"}`
9. Copy your Render backend URL (e.g. `https://portfolio-backend.onrender.com`)

---

## Step 5 — Deploy Celery Worker on Render

1. In Render dashboard → **New** → **Background Worker**
2. Connect the same `portfolio` GitHub repo
3. Configure:
   - **Name:** `portfolio-celery`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     celery -A app.tasks.worker worker --loglevel=info --concurrency=2
     ```
4. Choose **Free** plan
5. Add the **same environment variables** as Step 4 (all of them — Celery needs DB + Redis + GitHub token)
6. Click **Create Background Worker**

---

## Step 6 — Deploy Frontend on Vercel

### 6.1 — Add Vercel config

Create `frontend/vercel.json` to handle SPA routing:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/" }]
}
```

Commit and push this file:
```bash
git add frontend/vercel.json
git commit -m "add vercel SPA routing config"
git push
```

### 6.2 — Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Click **Add New Project**
3. Import your `portfolio` GitHub repo
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add environment variable:
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | `https://portfolio-backend.onrender.com` |
6. Click **Deploy**
7. Copy your Vercel URL (e.g. `https://portfolio-xyz.vercel.app`)

### 6.3 — Update CORS on Render

Go back to Render → `portfolio-backend` → Environment → update:

```
ALLOWED_ORIGINS=https://portfolio-xyz.vercel.app
```

Click **Save Changes** — Render will redeploy automatically.

---

## Step 7 — Verify everything works

Run through this checklist:

- [ ] `https://portfolio-backend.onrender.com/health` → `{"status":"ok"}`
- [ ] `https://portfolio-backend.onrender.com/api/v1/projects` → returns your projects JSON
- [ ] `https://portfolio-backend.onrender.com/api/v1/blog` → returns your blog posts JSON
- [ ] `https://portfolio-xyz.vercel.app` → loads your portfolio
- [ ] Projects page shows your projects
- [ ] Blog page shows your posts
- [ ] Contact form submits without error

---

## Custom Domain (optional)

### Vercel (frontend)
1. Vercel dashboard → your project → **Settings** → **Domains**
2. Add your domain → follow DNS instructions

### Render (backend)
1. Render dashboard → `portfolio-backend` → **Settings** → **Custom Domain**
2. Add your API domain (e.g. `api.yourdomain.com`)
3. Update `ALLOWED_ORIGINS` on Render to your real frontend domain
4. Update `VITE_API_URL` on Vercel to your real API domain

---

## Important limitations of free tier

| Issue | Impact | Workaround |
|-------|--------|------------|
| Render free service **sleeps after 15min idle** | First visit after idle takes ~30s | Accept it, or upgrade to $7/mo Starter |
| Upstash free tier: **10,000 req/day** | Enough for a portfolio | Monitor in Upstash dashboard |
| Neon free: **0.5 GB storage** | Plenty for a portfolio | Monitor in Neon dashboard |
| Celery beat (scheduler) won't run on free Background Worker | GitHub sync won't auto-run every 6h | Trigger manually via admin API, or upgrade |

---

## Ongoing maintenance

### Updating the app
```bash
# Make changes locally, test with docker-compose, then:
git add .
git commit -m "your change"
git push
# Render and Vercel auto-deploy on push to main
```

### Database migrations
When you add a new migration:
```bash
# Locally generate the migration
docker-compose exec backend alembic revision --autogenerate -m "description"
git add backend/alembic/versions/
git commit -m "add migration: description"
git push
# Render runs `alembic upgrade head` on every deploy (in the start command)
```

### Backing up Neon DB
```bash
pg_dump "postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require" \
  --no-owner --no-acl -F p -f backup_$(date +%Y%m%d).sql
```