from datetime import datetime

from pydantic import BaseModel


class PageViewCreate(BaseModel):
    path: str
    fingerprint: str | None = None
    duration_seconds: int | None = None


class AnalyticsSummary(BaseModel):
    total_visitors: int
    total_page_views: int
    today_visitors: int
    today_page_views: int
    top_pages: list[dict]           # [{path, views}]
    visitors_by_country: list[dict]
    visitors_by_day: list[dict]     # [{date, visitors, views}] last 30 days
    device_breakdown: list[dict]


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None   # for conversation memory


class ChatResponse(BaseModel):
    reply: str
    session_id: str