from sqlalchemy import Column, Integer, String, Float, Decimal, Date, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base


class ReportForecast(Base):
    __tablename__ = "report_forecast"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    report_date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    type = Column(String(32))
    profit_low = Column(Decimal(18, 4))
    profit_high = Column(Decimal(18, 4))
    profit_change_low = Column(Decimal(10, 4))
    profit_change_high = Column(Decimal(10, 4))
    change_reason = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class ReportExpress(Base):
    __tablename__ = "report_express"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    report_date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    revenue = Column(Decimal(18, 4))
    net_profit = Column(Decimal(18, 4))
    eps = Column(Decimal(10, 4))
    revenue_change = Column(Decimal(10, 4))
    net_profit_change = Column(Decimal(10, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class DividendData(Base):
    __tablename__ = "dividend_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    report_date = Column(Date, nullable=False)
    ex_date = Column(Date)
    pay_date = Column(Date)
    dividend_per_share = Column(Decimal(10, 4))
    bonus_share_ratio = Column(Decimal(10, 4))
    transfer_share_ratio = Column(Decimal(10, 4))
    plan_status = Column(String(32))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class AdjustFactor(Base):
    __tablename__ = "adjust_factor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    date = Column(Date, nullable=False)
    adjust_factor = Column(Decimal(18, 8), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())