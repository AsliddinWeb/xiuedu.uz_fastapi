"""
Backfill default body_p1/p2/link fields on HomeSection rows that were
created before these columns existed (notably 'intro').

Only fills NULL/empty values — won't overwrite admin edits.
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.home_settings import HomeSection

from scripts.seed_home import SECTION_DEFAULTS


async def main():
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(HomeSection))).scalars().all()
        updated = 0
        for row in rows:
            defaults = SECTION_DEFAULTS.get(row.key)
            if not defaults:
                continue
            changed = False
            for field, value in defaults.items():
                if getattr(row, field, None) in (None, ""):
                    setattr(row, field, value)
                    changed = True
            if changed:
                updated += 1
        await session.commit()
        print(f"[backfill] updated {updated} sections with defaults")


if __name__ == "__main__":
    asyncio.run(main())
