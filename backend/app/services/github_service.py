"""GitHub service — fetches public repos and syncs star/fork counts."""

from dataclasses import dataclass

import httpx

from app.core.config import settings

GITHUB_API = "https://api.github.com"


@dataclass
class GitHubRepo:
    name: str
    full_name: str
    description: str | None
    html_url: str
    homepage: str | None
    language: str | None
    stargazers_count: int
    forks_count: int
    topics: list[str]
    pushed_at: str
    archived: bool


async def fetch_user_repos(
    username: str | None = None,
    max_repos: int = 20,
) -> list[GitHubRepo]:
    username = username or settings.GITHUB_USERNAME
    headers = {"Accept": "application/vnd.github+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{GITHUB_API}/users/{username}/repos",
            headers=headers,
            params={"sort": "updated", "per_page": max_repos, "type": "owner"},
        )
        response.raise_for_status()
        data = response.json()

    return [
        GitHubRepo(
            name=r["name"],
            full_name=r["full_name"],
            description=r.get("description"),
            html_url=r["html_url"],
            homepage=r.get("homepage"),
            language=r.get("language"),
            stargazers_count=r["stargazers_count"],
            forks_count=r["forks_count"],
            topics=r.get("topics", []),
            pushed_at=r["pushed_at"],
            archived=r.get("archived", False),
        )
        for r in data
        if not r.get("archived") and not r.get("fork")
    ]


async def fetch_repo(repo_name: str) -> GitHubRepo:
    username = settings.GITHUB_USERNAME
    headers = {"Accept": "application/vnd.github+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{username}/{repo_name}",
            headers=headers,
        )
        response.raise_for_status()
        r = response.json()

    return GitHubRepo(
        name=r["name"],
        full_name=r["full_name"],
        description=r.get("description"),
        html_url=r["html_url"],
        homepage=r.get("homepage"),
        language=r.get("language"),
        stargazers_count=r["stargazers_count"],
        forks_count=r["forks_count"],
        topics=r.get("topics", []),
        pushed_at=r["pushed_at"],
        archived=r.get("archived", False),
    )