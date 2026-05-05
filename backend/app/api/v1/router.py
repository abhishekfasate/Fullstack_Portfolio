from fastapi import APIRouter

from app.api.v1.endpoints import analytics, auth, blog, chat, contact, github, projects, resume

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(blog.router)
api_router.include_router(contact.router)
api_router.include_router(chat.router)
api_router.include_router(github.router)
api_router.include_router(analytics.router)
api_router.include_router(resume.router)