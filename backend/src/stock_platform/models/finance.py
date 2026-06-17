from sqlalchemy import Column, Integer, String, Float, Decimal, Date, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base


class FinanceProfit(Base):
    __tablename__ = "finance_profit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    roe = Column(Decimal(10, 4))
    roa = Column(Decimal(10, 4))
    gross_profit_rate = Column(Decimal(10, 4))
    net_profit_rate = Column(Decimal(10, 4))
    eps = Column(Decimal(10, 4))
    total_share = Column(Decimal(18, 4))
    liqa_share = Column(Decimal(18, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class FinanceOperation(Base):
    __tablename__ = "finance_operation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    ar_turnover = Column(Decimal(10, 4))
    inventory_turnover = Column(Decimal(10, 4))
    current_asset_turnover = Column(Decimal(10, 4))
    total_asset_turnover = Column(Decimal(10, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class FinanceGrowth(Base):
    __tablename__ = "finance_growth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    revenue_growth_rate = Column(Decimal(10, 4))
    net_profit_growth_rate = Column(Decimal(10, 4))
    asset_growth_rate = Column(Decimal(10, 4))
    eps_growth_rate = Column(Decimal(10, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class FinanceBalance(Base):
    __tablename__ = "finance_balance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    asset_liability_ratio = Column(Decimal(10, 4))
    current_ratio = Column(Decimal(10, 4))
    quick_ratio = Column(Decimal(10, 4))
    interest_coverage_ratio = Column(Decimal(10, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class FinanceCashflow(Base):
    __tablename__ = "finance_cashflow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    operating_cash_flow = Column(Decimal(18, 4))
    investing_cash_flow = Column(Decimal(18, 4))
    financing_cash_flow = Column(Decimal(18, 4))
    free_cash_flow = Column(Decimal(18, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class FinanceDupont(Base):
    __tablename__ = "finance_dupont"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(16), ForeignKey("stocks.code"), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    roe = Column(Decimal(10, 4))
    net_profit_margin = Column(Decimal(10, 4))
    asset_turnover = Column(Decimal(10, 4))
    equity_multiplier = Column(Decimal(10, 4))
    created_at = Column(DateTime, nullable=False, server_default=func.now())