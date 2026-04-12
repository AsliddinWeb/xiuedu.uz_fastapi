"""One-shot: index all CMS content into chat chunks."""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import AsyncSessionLocal
from app.services.chat_indexer import reindex_all


async def main():
    async with AsyncSessionLocal() as session:
        count = await reindex_all(session)
        print(f"Indexed {count} content chunks")


if __name__ == "__main__":
    asyncio.run(main())
