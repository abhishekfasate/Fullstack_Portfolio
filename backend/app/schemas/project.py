from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ProjectBase(BaseModel):
    title: str
    summary: str
    description: str
    tech_stack: str
    github_url: str | None = None
    live_url: str | None = None
    thumbnail_url: str | None = None
    featured: bool = False
    order: int = 0
    is_published: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: str | None = None
    summary: str | None = None
    description: str | None = None
    tech_stack: str | None = None


class ProjectOut(ProjectBase):
    id: int
    slug: str
    stars: int
    forks: int
    created_at: datetime
    updated_at: datetime
    tech_list: list[str]

    model_config = {"from_attributes": True}