from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_admin, get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from slugify import slugify

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
async def list_projects(
    featured: bool | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[Project]:
    q = select(Project).where(Project.is_published == True).order_by(Project.order, Project.created_at.desc())
    if featured is not None:
        q = q.where(Project.featured == featured)
    result = await db.execute(q)
    return list(result.scalars())


@router.get("/{slug}", response_model=ProjectOut)
async def get_project(slug: str, db: AsyncSession = Depends(get_db)) -> Project:
    result = await db.execute(select(Project).where(Project.slug == slug, Project.is_published == True))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> Project:
    slug = slugify(data.title)
    # ensure uniqueness
    existing = await db.execute(select(Project).where(Project.slug == slug))
    if existing.scalar_one_or_none():
        slug = f"{slug}-2"
    project = Project(**data.model_dump(), slug=slug)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.patch("/{slug}", response_model=ProjectOut)
async def update_project(
    slug: str,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> Project:
    result = await db.execute(select(Project).where(Project.slug == slug))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    slug: str,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> None:
    result = await db.execute(select(Project).where(Project.slug == slug))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()