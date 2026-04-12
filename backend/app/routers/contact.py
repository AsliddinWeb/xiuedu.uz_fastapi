import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from app.middleware.rate_limit import limiter
from app.redis_client import redis_client

router = APIRouter(prefix="/contact", tags=["contact"])
log = logging.getLogger("xiuedu.contact")


class ContactMessage(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)
    subject: str = Field(min_length=2, max_length=200)
    message: str = Field(min_length=5, max_length=5000)


@router.post("", status_code=202)
async def submit(payload: ContactMessage):
    """Accept a contact form submission. Stores in a Redis list (FIFO)."""
    try:
        await redis_client.lpush(
            "contact:queue",
            payload.model_dump_json(),
        )
        await redis_client.ltrim("contact:queue", 0, 999)
    except Exception as e:  # noqa: BLE001
        log.exception("Failed to store contact message: %s", e)
        raise HTTPException(503, "Service temporarily unavailable")
    log.info("contact form: %s <%s>", payload.name, payload.email)
    return {"status": "accepted"}
