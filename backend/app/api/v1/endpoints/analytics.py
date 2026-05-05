from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_admin, get_db
from app.schemas.analytics import PageViewCreate
from app.services.analytics_service import get_summary, record_page_view

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/pageview", status_code=status.HTTP_204_NO_CONTENT)
async def track_page_view(
    data: PageViewCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> None:
    user_agent = request.headers.get("user-agent")
    ip = request.client.host if request.client else None
    await record_page_view(
        db,
        path=data.path,
        fingerprint=data.fingerprint,
        duration_seconds=data.duration_seconds,
        user_agent=user_agent,
        ip=ip,
    )


@router.get("/summary")
async def analytics_summary(
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    return await get_summary(db)