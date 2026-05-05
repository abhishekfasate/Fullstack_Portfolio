"""GitHub integration — returns live data from the GitHub API with Redis caching."""

import json

import redis.asyncio as aioredis
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.github_service import GitHubRepo, fetch_repo, fetch_user_repos

CACHE_TTL = 60 * 10   # 10 minutes

router = APIRouter(prefix="/github", tags=["github"])


async def _cached(key: str, fetch_fn, *args, **kwargs):
    r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        raw = await r.get(key)
        if raw:
            return json.loads(raw)
        data = await fetch_fn(*args, **kwargs)
        serialized = json.dumps([vars(d) for d in data] if isinstance(data, list) else vars(data))
        await r.setex(key, CACHE_TTL, serialized)
        return json.loads(serialized)
    finally:
        await r.close()


@router.get("/repos")
async def get_repos(max_repos: int = 12):
    try:
        data = await _cached("github:repos", fetch_user_repos, max_repos=max_repos)
        return data
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {exc}") from exc


@router.get("/repos/{repo_name}")
async def get_repo(repo_name: str):
    try:
        data = await _cached(f"github:repo:{repo_name}", fetch_repo, repo_name)
        return data
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {exc}") from exc