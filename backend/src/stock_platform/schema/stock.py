from pydantic import BaseModel, Field
from datetime import date, datetime


class StockResponse(BaseModel):
    code: str
    name: str
    industry_code: str | None
    exchange: str | None
    type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StockDetailResponse(BaseModel):
    code: str
    name: str
    industry_code: str | None
    industry_name: str | None
    exchange: str | None
    type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KLineDayResponse(BaseModel):
    id: int
    stock_code: str
    date: date
    open: float
    close: float
    high: float
    low: float
    volume: int
    amount: float | None
    pct_chg: float | None
    pe_ttm: float | None
    pb_mrq: float | None
    is_st: bool
    created_at: datetime

    class Config:
        from_attributes = True


class StockFilterRequest(BaseModel):
    industry_code: str | None = None
    type: str | None = None
    keyword: str | None = None
    page: int = 1
    page_size: int = 20