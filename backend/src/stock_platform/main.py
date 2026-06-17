from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from api.auth_router import router as auth_router
from api.stock_router import router as stock_router
from api.finance_router import router as finance_router
from api.task_router import router as task_router
from core.database import init_database
from core.settings import settings
import asyncio

app = FastAPI(
    title="HS Stock Platform API",
    description="股票数据采集与分析平台后端API，提供股票信息查询、财务数据、任务调度等功能，支持第三方系统和AI调用。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "HS Stock Platform Team",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(stock_router)
app.include_router(finance_router)
app.include_router(task_router)


@app.on_event("startup")
async def startup_event():
    await init_database()


@app.get("/")
async def root():
    return {"message": "hs-stock-platform backend API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}