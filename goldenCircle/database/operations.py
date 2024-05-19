from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from goldenCircle.types import ModelType


async def readAll(db: AsyncSession, limit: int, offset: int, ModelClass:ModelType):
    result = await db.execute(select(ModelClass).offset(offset).limit(limit))
    return result.scalars().all()


async def readById(db: AsyncSession, db_id: int, ModelClass:ModelType):
    result = await db.execute(select(ModelClass).filter(ModelClass.id == db_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Record Not Found.")
    return record


async def write(db: AsyncSession, db_id: int, ModelClass:ModelType, **kwargs):
    record = await readById(db, db_id, ModelClass=ModelClass)
    if record:
        for attr, value in kwargs.items():
            if not hasattr(record, attr):
                raise HTTPException(status_code=404,
                                    detail=f'{attr} Attribute does not exist. in <{ModelClass.__tablename__}> Model')
            if value is not None and hasattr(record, attr):
                setattr(record, attr, value)
        await db.commit()
        await db.refresh(record)
    return record


async def create(db: AsyncSession, ModelClass:ModelType, **kwargs: dict):
    record = ModelClass(**kwargs)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def delete(db: AsyncSession, db_id: int,ModelClass:ModelType):
    record = await readById(db, db_id, ModelClass=ModelClass)
    if record:
        await db.delete(record)
        await db.commit()
        return True
    return False
