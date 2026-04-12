"""
Backfill study_forms JSON from the old flat study_form/tuition/seats fields.
Each program gets 1 study form entry. Some programs get a second one
(part_time variant with lower tuition) for demonstration.
"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.home_settings import FacultyProgram


async def main():
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(FacultyProgram))).scalars().all()
        updated = 0
        for p in rows:
            if p.study_forms and len(p.study_forms) > 0:
                continue  # already backfilled

            forms = [
                {
                    "form": p.study_form or "full_time",
                    "tuition": p.tuition or "",
                    "seats": p.seats
                }
            ]

            # Give some bachelor programs a second (part_time) variant
            if p.level == "bachelor" and p.tuition:
                try:
                    # Parse "16 mln" → "12 mln" (75%)
                    num = int(''.join(c for c in p.tuition if c.isdigit()))
                    reduced = int(num * 0.75)
                    forms.append({
                        "form": "part_time",
                        "tuition": f"{reduced} mln",
                        "seats": max(1, (p.seats or 30) // 2)
                    })
                except (ValueError, TypeError):
                    pass

            p.study_forms = forms
            updated += 1

        await session.commit()
        print(f"Backfilled study_forms for {updated} programs")


if __name__ == "__main__":
    asyncio.run(main())
