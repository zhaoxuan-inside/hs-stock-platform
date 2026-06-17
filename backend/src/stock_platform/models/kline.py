from sqlalchemy import Column, Integer, String, Float, Decimal, Date, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base


class KLineDay(Base):
    __tablename__ = "kline_day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Decimal(10, 2), nullable=False)
    close = Column(Decimal(10, 2), nullable=False)
    high = Column(Decimal(10, 2), nullable=False)
    low = Column(Decimal(10, 2), nullable=False)
    volume = Column(Integer, nullable=False)
    amount = Column(Decimal(18, 2))
    pct_chg = Column(Decimal(6, 2))
    pe_ttm = Column(Decimal(10, 2))
    pb_mrq = Column(Decimal(10, 2))
    is_st = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class KLineWeek(Base):
    __tablename__ = "kline_week"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Decimal(10, 2), nullable=False)
    close = Column(Decimal(10, 2), nullable=False)
    high = Column(Decimal(10, 2), nullable=False)
    low = Column(Decimal(10, 2), nullable=False)
    volume = Column(Integer, nullable=False)
    amount = Column(Decimal(18, 2))
    pct_chg = Column(Decimal(6, 2))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class KLineMonth(Base):
    __tablename__ = "kline_month"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Decimal(10, 2), nullable=False)
    close = Column(Decimal(10, 2), nullable=False)
    high = Column(Decimal(10, 2), nullable=False)
    low = Column(Decimal(10, 2), nullable=False)
    volume = Column(Integer, nullable=False)
    amount = Column(Decimal(18, 2))
    pct_chg = Column(Decimal(6, 2))
    created_at = Column(DateTime, nullable=False, server_default=func.now())