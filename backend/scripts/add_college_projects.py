#!/usr/bin/env python
"""
One-time script to add NewsHub and Weather Reporting App projects.
Run from the backend/ directory:

    python scripts/add_college_projects.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, init_db
from app.models.project import Project

PROJECTS = [
    Project(
        title="NewsHub",
        slug="newshub",
        summary="A college project that aggregates and displays the latest news from multiple categories using a public news API.",
        description=(
            "## Overview\n\n"
            "NewsHub is a news aggregator web app built during college. "
            "It fetches real-time headlines from a public news API and displays them in a clean, readable layout.\n\n"
            "## Features\n\n"
            "- Browse news by category (Technology, Sports, Business, Entertainment)\n"
            "- Search for articles by keyword\n"
            "- Responsive card-based layout\n"
            "- Click-through to full articles\n\n"
            "## Tech Stack\n\n"
            "Built with vanilla JavaScript, HTML, and CSS. Uses the NewsAPI to fetch live headlines."
        ),
        tech_stack="JavaScript, HTML, CSS, NewsAPI",
        featured=False,
        order=2,
        is_published=True,
    ),
    Project(
        title="Weather Reporting App",
        slug="weather-reporting-app",
        summary="A college project that shows current weather and forecasts for any city using a weather API.",
        description=(
            "## Overview\n\n"
            "Weather Reporting App is a simple weather dashboard built during college. "
            "Enter any city name and instantly get current conditions along with a short-term forecast.\n\n"
            "## Features\n\n"
            "- Current temperature, humidity, and wind speed\n"
            "- 5-day weather forecast\n"
            "- Weather condition icons\n"
            "- City search with error handling for invalid inputs\n\n"
            "## Tech Stack\n\n"
            "Built with JavaScript, HTML, and CSS. Uses the OpenWeatherMap API for live weather data."
        ),
        tech_stack="JavaScript, HTML, CSS, OpenWeatherMap API",
        featured=False,
        order=3,
        is_published=True,
    ),
]


async def main():
    await init_db()

    async with AsyncSessionLocal() as db:
        for project in PROJECTS:
            existing = await db.execute(
                select(Project).where(Project.slug == project.slug)
            )
            if existing.scalar_one_or_none():
                print(f":warning:  Skipping '{project.title}' — already exists.")
            else:
                db.add(project)
                print(f":white_check_mark: Added '{project.title}'")

        await db.commit()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())