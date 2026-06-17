from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.finance import FinanceProfit, FinanceOperation, FinanceGrowth, FinanceBalance, FinanceCashflow, FinanceDupont
from models.report import ReportForecast, ReportExpress, DividendData, AdjustFactor


async def get_finance_profit(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceProfit | None:
    result = await db.execute(
        select(FinanceProfit)
        .where(FinanceProfit.stock_code == stock_code)
        .where(FinanceProfit.year == year)
        .where(FinanceProfit.quarter == quarter)
    )
    return result.scalar_one_or_none()


async def list_finance_profit(db: AsyncSession, stock_code: str, limit: int = 20):
    result = await db.execute(
        select(FinanceProfit)
        .where(FinanceProfit.stock_code == stock_code)
        .order_by(FinanceProfit.year.desc(), FinanceProfit.quarter.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_finance_operation(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceOperation | None:
    result = await db.execute(
        select(FinanceOperation)
        .where(FinanceOperation.stock_code == stock_code)
        .where(FinanceOperation.year == year)
        .where(FinanceOperation.quarter == quarter)
    )
    return result.scalar_one_or_none()


async def get_finance_growth(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceGrowth | None:
    result = await db.execute(
        select(FinanceGrowth)
        .where(FinanceGrowth.stock_code == stock_code)
        .where(FinanceGrowth.year == year)
        .where(FinanceGrowth.quarter == quarter)
    )
    return result.scalar_one_or_none()


async def get_finance_balance(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceBalance | None:
    result = await db.execute(
        select(FinanceBalance)
        .where(FinanceBalance.stock_code == stock_code)
        .where(FinanceBalance.year == year)
        .where(FinanceBalance.quarter == quarter)
    )
    return result.scalar_one_or_none()


async def get_finance_cashflow(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceCashflow | None:
    result = await db.execute(
        select(FinanceCashflow)
        .where(FinanceCashflow.stock_code == stock_code)
        .where(FinanceCashflow.year == year)
        .where(FinanceCashflow.quarter == quarter)
    )
    return result.scalar_one_or_none()


async def get_finance_dupont(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceDupont | None:
    result = await db.execute(
        select(FinanceDupont)
        .where(FinanceDupont.stock_code == stock_code)
        .where(FinanceDupont.year == year)
        .where(FinanceDupont.quarter == quarter)
    )
    return result.scalar_one_or_none()


async def list_report_forecast(db: AsyncSession, stock_code: str, limit: int = 20):
    result = await db.execute(
        select(ReportForecast)
        .where(ReportForecast.stock_code == stock_code)
        .order_by(ReportForecast.report_date.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def list_report_express(db: AsyncSession, stock_code: str, limit: int = 20):
    result = await db.execute(
        select(ReportExpress)
        .where(ReportExpress.stock_code == stock_code)
        .order_by(ReportExpress.report_date.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def list_dividend_data(db: AsyncSession, stock_code: str, limit: int = 20):
    result = await db.execute(
        select(DividendData)
        .where(DividendData.stock_code == stock_code)
        .order_by(DividendData.report_date.desc())
        .limit(limit)
    )
    return result.scalars().all()