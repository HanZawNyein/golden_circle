from database.base import engine, Base


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)