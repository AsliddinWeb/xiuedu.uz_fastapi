"""
SEO meta auto-generation helpers.

These functions derive meta_title / meta_description from the content
itself so admin users never have to fill SEO fields manually.
"""
import re

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_NBSP_RE = re.compile(r"&nbsp;|&#160;", re.IGNORECASE)


def strip_html(text: str | None) -> str:
    """Remove HTML tags and collapse whitespace."""
    if not text:
        return ""
    out = _NBSP_RE.sub(" ", text)
    out = _TAG_RE.sub(" ", out)
    out = _WS_RE.sub(" ", out).strip()
    return out


def truncate(text: str, limit: int) -> str:
    """Truncate at word boundary, append ellipsis if cut."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    # backtrack to last whitespace if reasonable
    space = cut.rfind(" ")
    if space > limit * 0.6:
        cut = cut[:space]
    return cut.rstrip(",.;:- ") + "…"


def auto_meta_title(title: str | None, *, limit: int = 60) -> str:
    """Build a meta_title from a content title."""
    return truncate(strip_html(title or ""), limit)


def auto_meta_description(*sources: str | None, limit: int = 160) -> str:
    """Build a meta_description from the first non-empty source.

    Tries each source in order (e.g. excerpt, then body) and returns the
    first one that yields non-empty stripped text.
    """
    for src in sources:
        clean = strip_html(src or "")
        if clean:
            return truncate(clean, limit)
    return ""


def fill_news_seo(data: dict) -> dict:
    """Populate meta_title_* / meta_description_* for news payload in-place.

    Only fills fields that are empty/None — never overwrites a value
    that an admin (or a previous auto-fill) already provided.
    """
    for lang in ("uz", "ru", "en"):
        title = data.get(f"title_{lang}") or ""
        excerpt = data.get(f"excerpt_{lang}") or ""
        body = data.get(f"body_{lang}") or ""
        mt_key = f"meta_title_{lang}"
        md_key = f"meta_description_{lang}"
        if not data.get(mt_key):
            data[mt_key] = auto_meta_title(title) or None
        if not data.get(md_key):
            data[md_key] = auto_meta_description(excerpt, body) or None
    return data


def fill_event_seo(data: dict) -> dict:
    """Same as fill_news_seo but for events (description instead of body)."""
    for lang in ("uz", "ru", "en"):
        title = data.get(f"title_{lang}") or ""
        description = data.get(f"description_{lang}") or ""
        mt_key = f"meta_title_{lang}"
        md_key = f"meta_description_{lang}"
        if not data.get(mt_key):
            data[mt_key] = auto_meta_title(title) or None
        if not data.get(md_key):
            data[md_key] = auto_meta_description(description) or None
    return data


def fill_page_seo(data: dict) -> dict:
    """Same for static pages (content field)."""
    for lang in ("uz", "ru", "en"):
        title = data.get(f"title_{lang}") or ""
        content = data.get(f"content_{lang}") or ""
        mt_key = f"meta_title_{lang}"
        md_key = f"meta_description_{lang}"
        if not data.get(mt_key):
            data[mt_key] = auto_meta_title(title) or None
        if not data.get(md_key):
            data[md_key] = auto_meta_description(content) or None
    return data
