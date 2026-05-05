"""Celery task — sync GitHub star/fork counts into the projects table."""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.project import Project
from app.services.github_service import fetch_repo
from app.tasks.worker import app


@app.task(name="app.tasks.github_sync.sync_all_repos", bind=True, max_retries=3)
def sync_all_repos(self):
    asyncio.run(_sync())


async def _sync():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Project).where(Project.github_url.isnot(None)))
        projects = result.scalars().all()

        for project in projects:
            try:
                repo_name = project.github_url.split("/")[-1]
                repo = await fetch_repo(repo_name)
                project.stars = repo.stargazers_count
                project.forks = repo.forks_count
            except Exception:
                pass

        await db.commit()