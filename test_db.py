import asyncio

from sqlalchemy import text

from app.core.database.session import engine


async def test_connection():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))

        print("Database Connected")
        print(result.scalar())


asyncio.run(test_connection())