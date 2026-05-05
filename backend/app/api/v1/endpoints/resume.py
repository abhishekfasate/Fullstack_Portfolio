"""Resume endpoint — serves a static PDF from S3 or local disk."""

import os
from pathlib import Path

import boto3
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

from app.core.config import settings

router = APIRouter(prefix="/resume", tags=["resume"])

LOCAL_RESUME_PATH = Path("static/resume.pdf")


@router.get("/download")
async def download_resume():
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_S3_BUCKET:
        # Generate a 1-hour pre-signed URL from S3
        s3 = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_S3_BUCKET, "Key": "resume.pdf"},
            ExpiresIn=3600,
        )
        return RedirectResponse(url=url)

    # Fallback: serve from local static directory
    if LOCAL_RESUME_PATH.exists():
        return FileResponse(
            path=LOCAL_RESUME_PATH,
            media_type="application/pdf",
            filename="resume.pdf",
        )

    raise HTTPException(status_code=404, detail="Resume not found")