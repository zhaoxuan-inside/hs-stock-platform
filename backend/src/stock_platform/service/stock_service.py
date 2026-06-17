from sqlalchemy.ext.asyncio import AsyncSession
from repository.stock_repository import get_stock_by_code, get_stock_detail, list_stocks, count_stocks, \
    get_kline_day, get_kline_week, get_kline_month, list_industries, list_indexes, get_index_constituents
from schema.stock import StockResponse, StockDetailResponse, KLineDayResponse
from fastapi import HTTPException, status
from datetime import date


async def get_stock(db: AsyncSession, code: str) -> StockResponse:
    stock = await get_stock_by_code(db, code)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="股票不存在")
    return StockResponse.model_validate(stock)


async def get_stock_detail_info(db: AsyncSession, code: str) -> StockDetailResponse:
    result = await get_stock_detail(db, code)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="股票不存在")
    stock, industry_name = result
    return StockDetailResponse(
        code=stock.code,
        name=stock.name,
        industry_code=stock.industry_code,
        industry_name=industry_name,
        exchange=stock.exchange,
        type=stock.type,
        created_at=stock.created_at,
        updated_at=stock.updated_at
    )


async def search_stocks(db: AsyncSession, industry_code: str | None = None,
                        type: str | None = None, keyword: str | None = None,
                        page: int = 1, page_size: int = 20):
    stocks = await list_stocks(db, industry_code, type, keyword, page, page_size)
    total = await count_stocks(db, industry_code, type, keyword)
    return {
        "data": [StockResponse.model_validate(stock) for stock in stocks],
        "total": total,
        "page": page,
        "page_size": page_size
    }


async def get_stock_kline_day(db: AsyncSession, stock_code: str, start_date: date | None = None,
                              end_date: date | None = None, limit: int = 100):
    kline_data = await get_kline_day(db, stock_code, start_date, end_date, limit)
    return [KLineDayResponse.model_validate(kline) for kline in kline_data]


async def get_stock_kline_week(db: AsyncSession, stock_code: str, start_date: date | None = None,
                               end_date: date | None = None, limit: int = 50):
    kline_data = await get_kline_week(db, stock_code, start_date, end_date, limit)
    return [KLineDayResponse.model_validate(kline) for kline in kline_data]


async def get_stock_kline_month(db: AsyncSession, stock_code: str, start_date: date | None = None,
                                end_date: date | None = None, limit: int = 24):
    kline_data = await get_kline_month(db, stock_code, start_date, end_date, limit)
    return [KLineDayResponse.model_validate(kline) for kline in kline_data]


async def get_all_industries(db: AsyncSession):
    industries = await list_industries(db)
    return industries


async def get_all_indexes(db: AsyncSession):
    indexes = await list_indexes(db)
    return indexes


async def get_index_stocks(db: AsyncSession, index_code: str):
    constituents = await get_index_constituents(db, index_code)
    return constituents