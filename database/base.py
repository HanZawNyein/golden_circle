from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('db_user')}:{os.getenv('db_passwd')}@{os.getenv('db_host')}/{os.getenv('db_name')}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()