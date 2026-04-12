from typing import Annotated, Literal

from fastapi import Header, Query

Lang = Literal["uz", "ru", "en"]
SUPPORTED: tuple[Lang, ...] = ("uz", "ru", "en")
DEFAULT: Lang = "uz"


def get_lang(
    lang: Annotated[str | None, Query()] = None,
    accept_language: Annotated[str | None, Header(alias="Accept-Language")] = None,
) -> Lang:
    if lang and lang in SUPPORTED:
        return lang  # type: ignore[return-value]
    if accept_language:
        for token in accept_language.split(","):
            code = token.strip().split(";")[0].split("-")[0].lower()
            if code in SUPPORTED:
                return code  # type: ignore[return-value]
    return DEFAULT


def pick(obj, base: str, lang: str, fallback: bool = True):
    """Get obj.{base}_{lang}; fall back to other locales if empty."""
    val = getattr(obj, f"{base}_{lang}", None)
    if val or not fallback:
        return val
    for code in SUPPORTED:
        v = getattr(obj, f"{base}_{code}", None)
        if v:
            return v
    return None
