"""
AI Chat models — content embeddings for RAG + conversation history.

Uses pgvector for semantic search over all CMS content.
Embedding dimension = 1024 (Groq's llama embeddings via API).
We use a simpler approach: content chunks stored as text with
tsvector full-text search + Groq LLM for generation.
This avoids the need for a separate embedding API call.
"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func, Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContentChunk(Base):
    """
    Pre-processed content chunks from all CMS pages.
    Each row = one paragraph/section of content with metadata.
    Full-text search via tsvector for retrieval.
    """
    __tablename__ = "chat_content_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Source info
    source_type: Mapped[str] = mapped_column(String(60), nullable=False)   # "faculty", "about", "faq", ...
    source_id:   Mapped[str] = mapped_column(String(60), default="", nullable=False)  # "pedagogika", "1", ...
    source_label: Mapped[str] = mapped_column(String(300), default="", nullable=False)  # human-readable

    # Multilingual content (stored separately for search)
    lang: Mapped[str] = mapped_column(String(5), nullable=False)  # "uz", "ru", "en"
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # PostgreSQL full-text search vector (auto-updated)
    tsv: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_chat_content_chunks_tsv", "tsv", postgresql_using="gin"),
    )


class ChatMessage(Base):
    """Simple conversation log — no auth required for public chat."""
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    session_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)  # anonymous session
    role:       Mapped[str] = mapped_column(String(20), nullable=False)  # "user" | "assistant"
    content:    Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
