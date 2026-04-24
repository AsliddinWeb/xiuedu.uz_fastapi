"""
Reset faculty programs with real XIU Edu data (2026 admission).

Deletes ALL existing faculties (cascade removes programs) and re-seeds from
the FACULTIES constant in seed_home.py. Use this on production to replace
any test/placeholder programs with the real admission flyer data.

Usage:
    cd backend
    source venv/bin/activate
    export $(grep -v '^#' ../.env.prod | xargs)
    python scripts/reset_faculties.py
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import delete
from app.database import AsyncSessionLocal
from app.models.home_settings import Faculty, FacultyProgram

from scripts.seed_home import FACULTIES


async def main():
    async with AsyncSessionLocal() as session:
        # Cascade-delete via ORM so FacultyProgram rows are removed too.
        await session.execute(delete(FacultyProgram))
        await session.execute(delete(Faculty))
        await session.commit()
        print("[reset] wiped all faculties and programs")

        total_programs = 0
        for i, f in enumerate(FACULTIES):
            data = dict(f)
            programs = data.pop("programs")
            fac = Faculty(sort_order=i, enabled=True, **data)
            session.add(fac)
            await session.flush()
            for j, p in enumerate(programs):
                prog = dict(p)
                sfs = prog.get("study_forms") or []
                if sfs:
                    first = sfs[0]
                    prog.setdefault("study_form", first.get("form", "full_time"))
                    prog.setdefault("tuition", first.get("tuition", ""))
                    prog.setdefault("seats", first.get("seats"))
                session.add(FacultyProgram(
                    faculty_id=fac.id, sort_order=j, enabled=True, **prog
                ))
                total_programs += 1

        await session.commit()
        print(f"[reset] inserted {len(FACULTIES)} faculties + {total_programs} programs")


if __name__ == "__main__":
    asyncio.run(main())
