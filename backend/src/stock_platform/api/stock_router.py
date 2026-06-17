from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schema.stock import StockResponse, StockDetailResponse
from service.stock_service import get_stock, get_stock_detail_info, search_stocks, \
    get_stock_kline_day, get_stock_kline_week, get_stock_kline_month, get_all_industries, \
    get_all_indexes, get_index_stocks
from core.database import get_db
from datetime import date

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/{code}", response_model=StockResponse)
async def get_stock_by_code(code: str, db: AsyncSession = Depends(get_db)):
    return await get_stock(db, code)


@router.get("/{code}/detail", response_model=StockDetailResponse)
async def get_stock_detail(code: str, db: AsyncSession = Depends(get_db)):
    return await get_stock_detail_info(db, code)


@router.get("/")
async def list_stocks(
    industry_code: str | None = Query(None),
    type: str | None = Query(None),
    keyword: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await search_stocks(db, industry_code, type, keyword, page, page_size)


@router.get("/{code}/kline/day")
async def get_kline_day(
    code: str,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    return await get_stock_kline_day(db, code, start_date, end_date, limit)


@router.get("/{code}/kline/week")
async def get_kline_week(
    code: str,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    return await get_stock_kline_week(db, code, start_date, end_date, limit)


@router.get("/{code}/kline/month")
async def get_kline_month(
    code: str,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    limit: int = Query(24, ge=1, le=120),
    db: AsyncSession = Depends(get_db)
):
    return await get_stock_kline_month(db, code, start_date, end_date, limit)


@router.get("/industries/list")
async def list_industries(db: AsyncSession = Depends(get_db)):
    return await get_all_industries(db)


@router.get("/indexes/list")
async def list_indexes(db: AsyncSession = Depends(get_db)):
    return await get_all_indexes(db)


@router.get("/indexes/{index_code}/constituents")
async def index_constituents(index_code: str, db: AsyncSession = Depends(get_db)):
    return await get_index_stocks(db, index_code)