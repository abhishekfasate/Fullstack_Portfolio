from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class ProjectTag(Base):
    __tablename__ = "project_tags"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    tag: Mapped[str] = mapped_column(String(50), primary_key=True)


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)          # card blurb
    description: Mapped[str] = mapped_column(Text, nullable=False)              # full case study (markdown)
    tech_stack: Mapped[str] = mapped_column(String(500), nullable=False)        # comma-separated
    github_url: Mapped[str | None] = mapped_column(String(500))
    live_url: Mapped[str | None] = mapped_column(String(500))
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    order: Mapped[int] = mapped_column(Integer, default=0)                      # sort order on page
    stars: Mapped[int] = mapped_column(Integer, default=0)                      # synced from GitHub
    forks: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    tags: Mapped[list[ProjectTag]] = relationship("ProjectTag", cascade="all, delete-orphan")

    @property
    def tech_list(self) -> list[str]:
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]