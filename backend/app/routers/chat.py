"""
AI Chat endpoint — RAG-powered by Groq + PostgreSQL full-text search.

Flow:
  1. User sends message + session_id + lang
  2. Full-text search over chat_content_chunks → top 5 results
  3. Build prompt: system message + context + conversation history + user message
  4. Call Groq API → get response
  5. Save both messages to chat_messages
  6. Return response (streaming not needed for now)
"""
import hashlib
import time
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.chat import ContentChunk, ChatMessage
from app.models.contact_page import ContactPage
from app.utils.lang import Lang, get_lang, pick

router = APIRouter(prefix="/chat", tags=["chat"])

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """Sen XIU Edu universitetining AI yordamchisisan. Ismini "XIU Yordamchi".

Javob berish qoidalari:
1. Faqat universitet haqidagi savollarga javob ber.
2. Javobni oddiy, qisqa va tushunarli ber — 2-3 gap yetarli.
3. Hech qachon "Sizning universitetimiz" yoki "Bizning universitet" dema. O'rniga universitetning nomini ishlatib, uchinchi shaxsda gapir. Misol: "XIU Edu Qarshi shahrida joylashgan." yoki "Universitet manzili: Qarshi shahri, I.Karimov ko'chasi 405-uy."
4. Narx, muddat, hujjat so'ralganda — faqat kontekstdagi aniq ma'lumotlarni ber.
5. Kontekstda javob yo'q bo'lsa — "Bu haqida aniq ma'lumotim yo'q. Qabul bo'limi bilan bog'laning:" deb quyidagi kontaktni ber.
6. Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob ber.
7. Ortiqcha gap ko'paytirma. Faqat kerakli ma'lumotni ber.

Kontaktlar:
📞 {phone}
📧 {email}
📍 {address}
"""


async def _search_chunks(session: AsyncSession, query: str, lang: str, limit: int = 6) -> list[ContentChunk]:
    """Full-text search over content chunks."""
    # Build tsquery from user input — split words, join with &
    words = [w.strip() for w in query.split() if len(w.strip()) > 1]
    if not words:
        return []

    # Use plainto_tsquery for simplicity (handles any input safely)
    stmt = (
        select(ContentChunk)
        .where(
            ContentChunk.lang == lang,
            ContentChunk.tsv.op("@@")(func.plainto_tsquery("simple", query))
        )
        .order_by(
            func.ts_rank(ContentChunk.tsv, func.plainto_tsquery("simple", query)).desc()
        )
        .limit(limit)
    )
    results = (await session.execute(stmt)).scalars().all()

    # If tsquery found nothing, fallback to ILIKE on first 3 words
    if not results and words:
        pattern = f"%{words[0]}%"
        stmt = (
            select(ContentChunk)
            .where(ContentChunk.lang == lang, ContentChunk.content.ilike(pattern))
            .limit(limit)
        )
        results = (await session.execute(stmt)).scalars().all()

    return results


async def _get_contact_info(session: AsyncSession, lang: str) -> dict:
    """Get contact details for the fallback message."""
    contact = (await session.execute(select(ContactPage).limit(1))).scalar_one_or_none()
    if not contact:
        return {"phone": "+998 55 406-15-15", "email": "info@xiuedu.uz", "address": "Toshkent"}
    return {
        "phone": contact.phone or "+998 55 406-15-15",
        "email": contact.email or "info@xiuedu.uz",
        "address": pick(contact, "address", lang) or "Toshkent",
    }


async def _get_history(session: AsyncSession, session_id: str, limit: int = 6) -> list[dict]:
    """Get recent conversation history."""
    rows = (await session.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(desc(ChatMessage.created_at))
        .limit(limit)
    )).scalars().all()
    return [{"role": m.role, "content": m.content} for m in reversed(rows)]


async def _call_groq(messages: list[dict]) -> str:
    """Call Groq API and return assistant response."""
    if not settings.GROQ_API_KEY:
        return "AI chat hozircha sozlanmagan. Iltimos, admin bilan bog'laning."

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.GROQ_MODEL,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 500,
            },
        )
        if resp.status_code != 200:
            return "Kechirasiz, hozir javob berishda muammo bor. Iltimos, keyinroq urinib ko'ring."
        data = resp.json()
        return data["choices"][0]["message"]["content"]


# ── Request / Response schemas ──
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None  # auto-generated if missing


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    sources: list[str] = []  # source labels for transparency


@router.post("/", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    lang: Annotated[Lang, Depends(get_lang)],
):
    if not payload.message or len(payload.message.strip()) < 2:
        raise HTTPException(400, "Message too short")

    # Session ID — generate if not provided
    session_id = payload.session_id or hashlib.md5(
        f"{time.time()}-{payload.message[:20]}".encode()
    ).hexdigest()

    user_msg = payload.message.strip()

    # 1. Search relevant content chunks
    chunks = await _search_chunks(db, user_msg, lang)

    # 2. Build context from chunks
    context_parts = []
    sources = []
    for c in chunks:
        context_parts.append(f"[{c.source_type}: {c.source_label}] {c.content}")
        if c.source_label and c.source_label not in sources:
            sources.append(c.source_label)

    context = "\n\n".join(context_parts) if context_parts else "Kontekst topilmadi."

    # 3. Get contact info for system prompt
    contact = await _get_contact_info(db, lang)
    system = SYSTEM_PROMPT.format(**contact)

    # 4. Get conversation history
    history = await _get_history(db, session_id)

    # 5. Build messages for LLM
    messages = [
        {"role": "system", "content": system},
        {"role": "system", "content": f"Quyidagi kontekst asosida javob ber:\n\n{context}"},
    ]
    messages.extend(history[-4:])  # last 2 exchanges
    messages.append({"role": "user", "content": user_msg})

    # 6. Call Groq
    reply = await _call_groq(messages)

    # 7. Save to history
    db.add(ChatMessage(session_id=session_id, role="user", content=user_msg))
    db.add(ChatMessage(session_id=session_id, role="assistant", content=reply))
    await db.commit()

    return ChatResponse(reply=reply, session_id=session_id, sources=sources[:5])
