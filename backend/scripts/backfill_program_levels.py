"""
Backfill the new fields on faculty_programs (level, study_form,
degree_*, credits, seats) for the rows seeded earlier.

Heuristic: programs with duration ending in "(M)" → master, ones with
duration in months → short courses, otherwise bachelor. MBA gets a
custom carve-out.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.home_settings import FacultyProgram


def infer_level(p: FacultyProgram) -> str:
    name = (p.name_uz or "").lower()
    dur = (p.duration_uz or "").lower()
    if "mba" in name:
        return "master"
    if "(m)" in dur or "(м)" in dur:
        return "master"
    if "oy" in dur or "месяц" in dur or "month" in dur:
        return "short"
    return "bachelor"


def degree_for(level: str) -> tuple[str, str, str]:
    if level == "master":
        return ("Magistr diplomi", "Диплом магистра", "Master's degree")
    if level == "short":
        return ("Sertifikat", "Сертификат", "Certificate")
    if level == "phd":
        return ("PhD", "PhD", "PhD")
    return ("Bakalavr diplomi", "Диплом бакалавра", "Bachelor's degree")


def credits_for(level: str) -> int:
    return {"bachelor": 240, "master": 120, "short": 12, "phd": 180}[level]


def seats_for(level: str) -> int:
    return {"bachelor": 50, "master": 25, "short": 30, "phd": 10}[level]


async def main():
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(FacultyProgram))).scalars().all()
        updated = 0
        for p in rows:
            level = infer_level(p)
            uz, ru, en = degree_for(level)
            p.level = level
            p.study_form = "full_time"
            if not p.degree_uz:
                p.degree_uz = uz
            if not p.degree_ru:
                p.degree_ru = ru
            if not p.degree_en:
                p.degree_en = en
            if p.credits is None:
                p.credits = credits_for(level)
            if p.seats is None:
                p.seats = seats_for(level)
            updated += 1
        await session.commit()
        print(f"Backfilled {updated} programs")


if __name__ == "__main__":
    asyncio.run(main())
