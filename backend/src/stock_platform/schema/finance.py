from pydantic import BaseModel
from datetime import datetime


class FinanceProfitResponse(BaseModel):
    id: int
    stock_code: str
    year: int
    quarter: int
    roe: float | None
    roa: float | None
    gross_profit_rate: float | None
    net_profit_rate: float | None
    eps: float | None
    total_share: float | None
    liqa_share: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FinanceOperationResponse(BaseModel):
    id: int
    stock_code: str
    year: int
    quarter: int
    ar_turnover: float | None
    inventory_turnover: float | None
    current_asset_turnover: float | None
    total_asset_turnover: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FinanceGrowthResponse(BaseModel):
    id: int
    stock_code: str
    year: int
    quarter: int
    revenue_growth_rate: float | None
    net_profit_growth_rate: float | None
    asset_growth_rate: float | None
    eps_growth_rate: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FinanceBalanceResponse(BaseModel):
    id: int
    stock_code: str
    year: int
    quarter: int
    asset_liability_ratio: float | None
    current_ratio: float | None
    quick_ratio: float | None
    interest_coverage_ratio: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FinanceCashflowResponse(BaseModel):
    id: int
    stock_code: str
    year: int
    quarter: int
    operating_cash_flow: float | None
    investing_cash_flow: float | None
    financing_cash_flow: float | None
    free_cash_flow: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FinanceDupontResponse(BaseModel):
    id: int
    stock_code: str
    year: int
    quarter: int
    roe: float | None
    net_profit_margin: float | None
    asset_turnover: float | None
    equity_multiplier: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FinanceSummaryResponse(BaseModel):
    profit: FinanceProfitResponse | None
    operation: FinanceOperationResponse | None
    growth: FinanceGrowthResponse | None
    balance: FinanceBalanceResponse | None
    cashflow: FinanceCashflowResponse | None
    dupont: FinanceDupontResponse | None