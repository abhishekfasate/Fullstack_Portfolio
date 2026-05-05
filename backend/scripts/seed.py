#!/usr/bin/env python
"""
Seed the database with the admin user and sample projects/blog posts.
Run once after `alembic upgrade head`:

    python scripts/seed.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.database import AsyncSessionLocal, init_db
from app.core.security import hash_password
from app.models.admin import Admin
from app.models.blog import BlogPost, Tag
from app.models.project import Project


async def seed():
    await init_db()

    async with AsyncSessionLocal() as db:
        # Admin
        db.add(Admin(email="admin@example.com", hashed_password=hash_password("changeme")))

        # Projects
        db.add(Project(
            title="Portfolio API",
            slug="portfolio-api",
            summary="The FastAPI backend powering this portfolio.",
            description="## Overview\n\nBuilt with FastAPI, SQLAlchemy, and PostgreSQL...",
            tech_stack="Python, FastAPI, PostgreSQL, Redis, Docker",
            github_url="https://github.com/johndoe/portfolio-api",
            featured=True,
            order=1,
        ))

        db.add(Project(
            title="NewsHub",
            slug="newshub",
            summary="A college project that aggregates and displays the latest news from multiple categories using a public news API.",
            description="## Overview\n\nNewsHub is a news aggregator web app built during college. It fetches real-time headlines from a public news API and displays them in a clean, readable layout.\n\n## Features\n\n- Browse news by category (Technology, Sports, Business, Entertainment)\n- Search for articles by keyword\n- Responsive card-based layout\n- Click-through to full articles\n\n## Tech Stack\n\nBuilt with vanilla JavaScript, HTML, and CSS. Uses the NewsAPI to fetch live headlines.",
            tech_stack="JavaScript, HTML, CSS, NewsAPI",
            featured=False,
            order=2,
            is_published=True,
        ))

        db.add(Project(
            title="Weather Reporting App",
            slug="weather-reporting-app",
            summary="A college project that shows current weather and forecasts for any city using a weather API.",
            description="## Overview\n\nWeather Reporting App is a simple weather dashboard built during college. Enter any city name and instantly get current conditions along with a short-term forecast.\n\n## Features\n\n- Current temperature, humidity, and wind speed\n- 5-day weather forecast\n- Weather condition icons\n- City search with error handling for invalid inputs\n\n## Tech Stack\n\nBuilt with JavaScript, HTML, and CSS. Uses the OpenWeatherMap API for live weather data.",
            tech_stack="JavaScript, HTML, CSS, OpenWeatherMap API",
            featured=False,
            order=3,
            is_published=True,
        ))

        # Blog tag + post
        python_tag = Tag(name="Python", slug="python")
        devops_tag = Tag(name="DevOps", slug="devops")
        db.add_all([python_tag, devops_tag])

        post = BlogPost(
            title="Building a Production FastAPI App from Scratch",
            slug="building-production-fastapi-app",
            excerpt="Lessons learned deploying a FastAPI + PostgreSQL app to a VPS with Docker and Nginx.",
            content="## Introduction\n\nThis is my first blog post...",
            reading_time_minutes=8,
            is_published=True,
            featured=True,
        )
        post.tags = [python_tag, devops_tag]
        db.add(post)

        await db.commit()
        print(":white_check_mark: Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())