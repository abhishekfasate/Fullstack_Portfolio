from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    posts: Mapped[list["BlogPost"]] = relationship("BlogPost", secondary="blog_post_tags", back_populates="tags")


class BlogPostTag(Base):
    __tablename__ = "blog_post_tags"

    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class BlogPost(Base, TimestampMixin):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    slug: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    excerpt: Mapped[str] = mapped_column(String(600), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)                 # markdown
    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    reading_time_minutes: Mapped[int] = mapped_column(Integer, default=5)
    views: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)

    tags: Mapped[list[Tag]] = relationship("Tag", secondary="blog_post_tags", back_populates="posts")