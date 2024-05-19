from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Sequence
from . import Base


async def readAll(db: AsyncSession, limit: int, offset: int, ModelClass):
    result = await db.execute(select(ModelClass).offset(offset).limit(limit))
    return result.scalars().all()
