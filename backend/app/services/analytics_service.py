"""Analytics service — record page views and build dashboard summaries."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics import PageView, VisitorSession


async def record_page_view(
    db: AsyncSession,
    path: str,
    fingerprint: str | None,
    duration_seconds: int | None,
    user_agent: str | None,
    ip: str | None,
) -> None:
    # Upsert visitor session
    if fingerprint:
        result = await db.execute(
            select(VisitorSession).where(VisitorSession.fingerprint == fingerprint)
        )
        session = result.scalar_one_or_none()
        if session:
            session.last_seen = datetime.now(timezone.utc)
            session.visit_count += 1
        else:
            device = _parse_device(user_agent)
            browser = _parse_browser(user_agent)
            db.add(
                VisitorSession(
                    fingerprint=fingerprint,
                    device_type=device,
                    browser=browser,
                )
            )

    db.add(PageView(path=path, fingerprint=fingerprint, duration_seconds=duration_seconds))
    await db.commit()


async def get_summary(db: AsyncSession) -> dict:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    thirty_days_ago = now - timedelta(days=30)

    total_visitors = await db.scalar(select(func.count()).select_from(VisitorSession))
    total_views = await db.scalar(select(func.count()).select_from(PageView))

    today_visitors_q = select(func.count()).select_from(VisitorSession).where(
        VisitorSession.last_seen >= today_start
    )
    today_visitors = await db.scalar(today_visitors_q)

    today_views_q = select(func.count()).select_from(PageView).where(
        PageView.viewed_at >= today_start
    )
    today_views = await db.scalar(today_views_q)

    # Top pages (last 30 days)
    top_pages_q = (
        select(PageView.path, func.count().label("views"))
        .where(PageView.viewed_at >= thirty_days_ago)
        .group_by(PageView.path)
        .order_by(func.count().desc())
        .limit(10)
    )
    top_pages_result = await db.execute(top_pages_q)
    top_pages = [{"path": r.path, "views": r.views} for r in top_pages_result]

    # Device breakdown
    device_q = (
        select(VisitorSession.device_type, func.count().label("count"))
        .group_by(VisitorSession.device_type)
    )
    device_result = await db.execute(device_q)
    device_breakdown = [{"device": r.device_type or "unknown", "count": r.count} for r in device_result]

    return {
        "total_visitors": total_visitors or 0,
        "total_page_views": total_views or 0,
        "today_visitors": today_visitors or 0,
        "today_page_views": today_views or 0,
        "top_pages": top_pages,
        "visitors_by_country": [],   # populate with geo-ip in production
        "visitors_by_day": [],       # populate with a date-series query
        "device_breakdown": device_breakdown,
    }


# ── Lightweight UA parsers (no external dep needed) ───────────────────────────

def _parse_device(ua: str | None) -> str:
    if not ua:
        return "unknown"
    ua = ua.lower()
    if any(t in ua for t in ("mobile", "android", "iphone")):
        return "mobile"
    if "tablet" in ua or "ipad" in ua:
        return "tablet"
    return "desktop"


def _parse_browser(ua: str | None) -> str:
    if not ua:
        return "unknown"
    ua = ua.lower()
    for name in ("firefox", "chrome", "safari", "edge", "opera"):
        if name in ua:
            return name
    return "other"