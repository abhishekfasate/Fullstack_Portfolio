from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.deps import get_current_admin, get_db
from app.models.blog import BlogPost, Tag
from app.schemas.blog import BlogPostCreate, BlogPostListOut, BlogPostOut, BlogPostUpdate, TagOut
from slugify import slugify

router = APIRouter(prefix="/blog", tags=["blog"])


@router.get("/tags", response_model=list[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db)) -> list[Tag]:
    result = await db.execute(select(Tag).order_by(Tag.name))
    return list(result.scalars())


@router.get("", response_model=list[BlogPostListOut])
async def list_posts(
    tag: str | None = Query(None, description="Filter by tag slug"),
    featured: bool | None = None,
    limit: int = Query(10, le=50),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[BlogPost]:
    q = (
        select(BlogPost)
        .options(selectinload(BlogPost.tags))
        .where(BlogPost.is_published == True)
        .order_by(BlogPost.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if featured is not None:
        q = q.where(BlogPost.featured == featured)
    if tag:
        q = q.join(BlogPost.tags).where(Tag.slug == tag)
    result = await db.execute(q)
    return list(result.scalars())


@router.get("/{slug}", response_model=BlogPostOut)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)) -> BlogPost:
    result = await db.execute(
        select(BlogPost)
        .options(selectinload(BlogPost.tags))
        .where(BlogPost.slug == slug, BlogPost.is_published == True)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.views += 1  # bump view counter
    await db.commit()
    return post


@router.post("", response_model=BlogPostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> BlogPost:
    slug = slugify(data.title)
    tag_ids = data.tag_ids
    post = BlogPost(**data.model_dump(exclude={"tag_ids"}), slug=slug)
    if tag_ids:
        tags_result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        post.tags = list(tags_result.scalars())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.patch("/{slug}", response_model=BlogPostOut)
async def update_post(
    slug: str,
    data: BlogPostUpdate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> BlogPost:
    result = await db.execute(
        select(BlogPost).options(selectinload(BlogPost.tags)).where(BlogPost.slug == slug)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)
    for field, value in update_data.items():
        setattr(post, field, value)
    if tag_ids is not None:
        tags_result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        post.tags = list(tags_result.scalars())
    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    slug: str,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
) -> None:
    result = await db.execute(select(BlogPost).where(BlogPost.slug == slug))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()