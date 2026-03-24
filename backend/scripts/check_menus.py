import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import db_getter


async def check_menus():
    async_session = db_getter()
    db = await async_session.__anext__()

    result = await db.execute(
        text(
            "SELECT id, menu_name, path, component FROM sys_menu WHERE path IN ('cloud-map', 'mainforce')"
        )
    )
    rows = result.fetchall()

    print("ID | menu_name | path | component")
    print("-" * 80)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")

    await db.close()


if __name__ == "__main__":
    asyncio.run(check_menus())
