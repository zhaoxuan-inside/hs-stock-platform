from sqlalchemy.ext.asyncio import AsyncSession
from repository.auth_repository import get_user_by_username, create_user, verify_password
from schema.auth import UserCreate, LoginRequest, LoginResponse
from core.settings import settings
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from models.base import User
from uuid import UUID


async def register_user(db: AsyncSession, user_create: UserCreate) -> User:
    existing_user = await get_user_by_username(db, user_create.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    return await create_user(db, user_create)


async def login_user(db: AsyncSession, login_request: LoginRequest) -> LoginResponse:
    user = await get_user_by_username(db, login_request.username)
    if not user or not await verify_password(login_request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return LoginResponse(access_token=access_token)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_current_user(db: AsyncSession, token: str) -> User:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌验证失败")
    
    user = await db.get(User, UUID(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")
    return user