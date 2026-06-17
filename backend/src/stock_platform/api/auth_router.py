from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schema.auth import UserCreate, LoginRequest, LoginResponse, UserResponse
from service.auth_service import register_user, login_user, get_current_user
from core.database import get_db
from models.base import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, user_create)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(db, login_request)


@router.get("/me", response_model=UserResponse)
async def get_me(token: str, db: AsyncSession = Depends(get_db)):
    user = await get_current_user(db, token)
    return user