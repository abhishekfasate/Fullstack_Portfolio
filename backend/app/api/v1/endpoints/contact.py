import asyncio

from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db
from app.models.contact import ContactMessage
from app.schemas.contact import ContactCreate, ContactOut
from app.services.email_service import send_auto_reply, send_contact_email

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
async def submit_contact(
    data: ContactCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ContactMessage:
    ip = request.client.host if request.client else None

    msg = ContactMessage(
        name=data.name,
        email=data.email,
        subject=data.subject,
        message=data.message,
        ip_address=ip,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)

    # Fire-and-forget — don't block the response on email delivery
    background_tasks.add_task(send_contact_email, data.name, data.email, data.subject, data.message)
    background_tasks.add_task(send_auto_reply, data.name, data.email)

    return msg