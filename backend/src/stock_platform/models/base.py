from sqlalchemy import Column, Integer, String, Float, Decimal, Date, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(32), nullable=False, default="user")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Stock(Base):
    __tablename__ = "stocks"

    code = Column(String(16), primary_key=True)
    name = Column(String(64), nullable=False)
    industry_code = Column(String(16), ForeignKey("industry.code"))
    exchange = Column(String(32))
    type = Column(String(16), default="stock")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Industry(Base):
    __tablename__ = "industry"

    code = Column(String(16), primary_key=True)
    name = Column(String(64), nullable=False)
    parent_code = Column(String(16), ForeignKey("industry.code"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class StockIndustry(Base):
    __tablename__ = "stock_industry"

    stock_code = Column(String(16), ForeignKey("stocks.code"), primary_key=True)
    industry_code = Column(String(16), ForeignKey("industry.code"), primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class StockIndex(Base):
    __tablename__ = "stock_index"

    code = Column(String(16), primary_key=True)
    name = Column(String(64), nullable=False)
    type = Column(String(32))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class IndexConstituent(Base):
    __tablename__ = "index_constituent"

    index_code = Column(String(16), ForeignKey("stock_index.code"), primary_key=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), primary_key=True)
    entry_date = Column(Date)
    exit_date = Column(Date)
    created_at = Column(DateTime, nullable=False, server_default=func.now())