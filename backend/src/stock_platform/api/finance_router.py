from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schema.finance import FinanceSummaryResponse, FinanceProfitResponse
from service.finance_service import get_finance_summary, get_profit_history, \
    get_report_forecast, get_report_express, get_dividend_history
from core.database import get_db

router = APIRouter(prefix="/finance", tags=["finance"])


@router.get("/{stock_code}/summary", response_model=FinanceSummaryResponse)
async def finance_summary(
    stock_code: str,
    year: int = Query(..., ge=2000),
    quarter: int = Query(..., ge=1, le=4),
    db: AsyncSession = Depends(get_db)
):
    return await get_finance_summary(db, stock_code, year, quarter)


@router.get("/{stock_code}/profit")
async def profit_history(
    stock_code: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await get_profit_history(db, stock_code, limit)


@router.get("/{stock_code}/report/forecast")
async def report_forecast(
    stock_code: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await get_report_forecast(db, stock_code, limit)


@router.get("/{stock_code}/report/express")
async def report_express(
    stock_code: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await get_report_express(db, stock_code, limit)


@router.get("/{stock_code}/dividend")
async def dividend_history(
    stock_code: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await get_dividend_history(db, stock_code, limit)