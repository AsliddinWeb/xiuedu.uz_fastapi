from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.media import MediaFile
from app.models.user import User, Role
from app.schemas.common import Paginated
from app.schemas.media import MediaAltUpdate, MediaOut, MediaUploadResponse
from app.services.image_service import IMAGE_MIMES, delete_file, process_upload
from app.utils.deps import CurrentUser, require_roles

router = APIRouter(prefix="/admin/media", tags=["admin:media"])
_dep = require_roles(Role.ADMIN, Role.CONTENT_MANAGER, Role.PAGE_EDITOR)


@router.post("/upload", response_model=MediaUploadResponse, status_code=201)
async def upload_media(
    file: UploadFile,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(_dep),
):
    info = await process_upload(file)
    media = MediaFile(
        filename=info["filename"],
        original_name=info["original_name"],
        mime_type=info["mime_type"],
        size_bytes=info["size_bytes"],
        url=info["url"],
        width=info["width"],
        height=info["height"],
        uploaded_by=user.id,
    )
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return MediaUploadResponse(
        id=media.id,
        url=media.url,
        thumbnail_url=info["thumbnail_url"],
        medium_url=info["medium_url"],
        filename=media.filename,
        size_bytes=media.size_bytes,
        mime_type=media.mime_type,
        width=media.width,
        height=media.height,
    )


@router.get("/", response_model=Paginated[MediaOut])
async def list_media(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    limit: int = Query(24, ge=1, le=200),
    type: str | None = Query(None, description="image | document"),
    _u: User = Depends(_dep),
):
    stmt = select(MediaFile)
    if type == "image":
        stmt = stmt.where(MediaFile.mime_type.in_(list(IMAGE_MIMES)))
    elif type == "document":
        stmt = stmt.where(~MediaFile.mime_type.in_(list(IMAGE_MIMES)))

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (
        await db.execute(
            stmt.order_by(MediaFile.id.desc()).offset((page - 1) * limit).limit(limit)
        )
    ).scalars().all()
    return Paginated[MediaOut](
        items=rows,
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@router.patch("/{media_id}/alt", response_model=MediaOut)
async def update_alt(
    media_id: int,
    payload: MediaAltUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    m = await db.get(MediaFile, media_id)
    if not m:
        raise HTTPException(404, "Media not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(m, k, v)
    await db.commit()
    await db.refresh(m)
    return m


@router.delete("/{media_id}", status_code=204)
async def delete_media(
    media_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _u: User = Depends(_dep),
):
    m = await db.get(MediaFile, media_id)
    if not m:
        raise HTTPException(404, "Media not found")
    delete_file(m.url)
    await db.delete(m)
    await db.commit()
