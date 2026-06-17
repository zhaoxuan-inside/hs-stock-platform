from sqlalchemy.ext.asyncio import AsyncSession
from repository.finance_repository import get_finance_profit, get_finance_operation, get_finance_growth, \
    get_finance_balance, get_finance_cashflow, get_finance_dupont, list_report_forecast, \
    list_report_express, list_dividend_data
from schema.finance import FinanceProfitResponse, FinanceOperationResponse, FinanceGrowthResponse, \
    FinanceBalanceResponse, FinanceCashflowResponse, FinanceDupontResponse, FinanceSummaryResponse


async def get_finance_summary(db: AsyncSession, stock_code: str, year: int, quarter: int) -> FinanceSummaryResponse:
    profit = await get_finance_profit(db, stock_code, year, quarter)
    operation = await get_finance_operation(db, stock_code, year, quarter)
    growth = await get_finance_growth(db, stock_code, year, quarter)
    balance = await get_finance_balance(db, stock_code, year, quarter)
    cashflow = await get_finance_cashflow(db, stock_code, year, quarter)
    dupont = await get_finance_dupont(db, stock_code, year, quarter)
    
    return FinanceSummaryResponse(
        profit=FinanceProfitResponse.model_validate(profit) if profit else None,
        operation=FinanceOperationResponse.model_validate(operation) if operation else None,
        growth=FinanceGrowthResponse.model_validate(growth) if growth else None,
        balance=FinanceBalanceResponse.model_validate(balance) if balance else None,
        cashflow=FinanceCashflowResponse.model_validate(cashflow) if cashflow else None,
        dupont=FinanceDupontResponse.model_validate(dupont) if dupont else None
    )


async def get_profit_history(db: AsyncSession, stock_code: str, limit: int = 20):
    data = await list_finance_profit(db, stock_code, limit)
    return [FinanceProfitResponse.model_validate(item) for item in data]


async def get_report_forecast(db: AsyncSession, stock_code: str, limit: int = 20):
    data = await list_report_forecast(db, stock_code, limit)
    return data


async def get_report_express(db: AsyncSession, stock_code: str, limit: int = 20):
    data = await list_report_express(db, stock_code, limit)
    return data


async def get_dividend_history(db: AsyncSession, stock_code: str, limit: int = 20):
    data = await list_dividend_data(db, stock_code, limit)
    return data