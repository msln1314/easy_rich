import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import db_getter


async def fix_menu_component():
    async_session = db_getter()
    db = await async_session.__anext__()

    try:
        await db.execute(
            text(
                "UPDATE sys_menu SET component = 'views/Vadmin/Stock/MarketCloudMap/MarketCloudMap' WHERE path = 'cloud-map'"
            )
        )
        print("Updated cloud-map component path")

        await db.execute(
            text(
                "UPDATE sys_menu SET component = 'views/Vadmin/Stock/Fund/MainForce' WHERE path = 'mainforce'"
            )
        )
        print("Updated mainforce component path")

        await db.commit()
        print("Done!")

    except Exception as e:
        await db.rollback()
        print(f"Error: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(fix_menu_component())
