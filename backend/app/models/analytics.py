from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VisitorSession(Base):
    """One row per unique visitor (keyed by fingerprint hash)."""

    __tablename__ = "visitor_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    country: Mapped[str | None] = mapped_column(String(80))
    city: Mapped[str | None] = mapped_column(String(120))
    device_type: Mapped[str | None] = mapped_column(String(40))               # mobile | tablet | desktop
    browser: Mapped[str | None] = mapped_column(String(80))
    os: Mapped[str | None] = mapped_column(String(80))
    referrer: Mapped[str | None] = mapped_column(String(500))
    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    visit_count: Mapped[int] = mapped_column(Integer, default=1)


class PageView(Base):
    """One row per page visit event."""

    __tablename__ = "page_views"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String(500), index=True, nullable=False)
    fingerprint: Mapped[str | None] = mapped_column(String(64), index=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )