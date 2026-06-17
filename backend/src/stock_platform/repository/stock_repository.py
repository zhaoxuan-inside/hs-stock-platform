from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from models.base import Stock, Industry, StockIndustry, StockIndex, IndexConstituent
from models.kline import KLineDay, KLineWeek, KLineMonth
from datetime import date


async def get_stock_by_code(db: AsyncSession, code: str) -> Stock | None:
    result = await db.execute(select(Stock).where(Stock.code == code))
    return result.scalar_one_or_none()


async def get_stock_detail(db: AsyncSession, code: str):
    result = await db.execute(
        select(Stock, Industry.name.label('industry_name'))
        .outerjoin(Industry, Stock.industry_code == Industry.code)
        .where(Stock.code == code)
    )
    return result.first()


async def list_stocks(db: AsyncSession, industry_code: str | None = None,
                      type: str | None = None, keyword: str | None = None,
                      page: int = 1, page_size: int = 20):
    query = select(Stock)
    
    filters = []
    if industry_code:
        filters.append(Stock.industry_code == industry_code)
    if type:
        filters.append(Stock.type == type)
    if keyword:
        filters.append(or_(Stock.code.contains(keyword), Stock.name.contains(keyword)))
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.order_by(Stock.code).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    return result.scalars().all()


async def count_stocks(db: AsyncSession, industry_code: str | None = None,
                       type: str | None = None, keyword: str | None = None) -> int:
    query = select(Stock)
    
    filters = []
    if industry_code:
        filters.append(Stock.industry_code == industry_code)
    if type:
        filters.append(Stock.type == type)
    if keyword:
        filters.append(or_(Stock.code.contains(keyword), Stock.name.contains(keyword)))
    
    if filters:
        query = query.where(and_(*filters))
    
    result = await db.execute(select(func.count()).select_from(query.subquery()))
    return result.scalar()


async def get_kline_day(db: AsyncSession, stock_code: str, start_date: date | None = None,
                        end_date: date | None = None, limit: int = 100):
    query = select(KLineDay).where(KLineDay.stock_code == stock_code)
    
    if start_date:
        query = query.where(KLineDay.date >= start_date)
    if end_date:
        query = query.where(KLineDay.date <= end_date)
    
    query = query.order_by(KLineDay.date.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_kline_week(db: AsyncSession, stock_code: str, start_date: date | None = None,
                         end_date: date | None = None, limit: int = 50):
    query = select(KLineWeek).where(KLineWeek.stock_code == stock_code)
    
    if start_date:
        query = query.where(KLineWeek.date >= start_date)
    if end_date:
        query = query.where(KLineWeek.date <= end_date)
    
    query = query.order_by(KLineWeek.date.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_kline_month(db: AsyncSession, stock_code: str, start_date: date | None = None,
                          end_date: date | None = None, limit: int = 24):
    query = select(KLineMonth).where(KLineMonth.stock_code == stock_code)
    
    if start_date:
        query = query.where(KLineMonth.date >= start_date)
    if end_date:
        query = query.where(KLineMonth.date <= end_date)
    
    query = query.order_by(KLineMonth.date.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def list_industries(db: AsyncSession):
    result = await db.execute(select(Industry).order_by(Industry.code))
    return result.scalars().all()


async def list_indexes(db: AsyncSession):
    result = await db.execute(select(StockIndex).order_by(StockIndex.code))
    return result.scalars().all()


async def get_index_constituents(db: AsyncSession, index_code: str):
    result = await db.execute(
        select(IndexConstituent, Stock)
        .join(Stock, IndexConstituent.stock_code == Stock.code)
        .where(IndexConstituent.index_code == index_code)
    )
    return result.all()


from sqlalchemy import func