from fastapi.exceptions import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def readAll(db: AsyncSession, limit: int, offset: int, ModelClass):
    result = await db.execute(select(ModelClass).offset(offset).limit(limit))
    return result.scalars().all()


async def readById(db: AsyncSession, db_id: int, ModelClass):
    result = await db.execute(select(ModelClass).filter(ModelClass.id == db_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Record Not Found.")
    return record
