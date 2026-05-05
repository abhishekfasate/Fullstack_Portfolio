from datetime import datetime

from pydantic import BaseModel


class TagOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class BlogPostBase(BaseModel):
    title: str
    excerpt: str
    content: str
    cover_image_url: str | None = None
    reading_time_minutes: int = 5
    is_published: bool = False
    featured: bool = False


class BlogPostCreate(BlogPostBase):
    tag_ids: list[int] = []


class BlogPostUpdate(BlogPostBase):
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    tag_ids: list[int] | None = None


class BlogPostOut(BlogPostBase):
    id: int
    slug: str
    views: int
    tags: list[TagOut]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BlogPostListOut(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str
    cover_image_url: str | None
    reading_time_minutes: int
    views: int
    tags: list[TagOut]
    featured: bool
    created_at: datetime

    model_config = {"from_attributes": True}