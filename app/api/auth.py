from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, get_current_user
from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.schemas.base import APIResponse
from app.services.auth import AuthService
from fastapi.security import HTTPBearer


router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/register", response_model=APIResponse[TokenResponse])
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.register(data)
    return APIResponse(
        success=True, data=result, message="Usuario registrado exitosamente"
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.login(data)
    return APIResponse(success=True, data=result, message="Sesión iniciada")


security = HTTPBearer()


@router.get("/me", response_model=APIResponse[UserResponse])
async def me(current_user: UserResponse = Depends(get_current_user)):
    return APIResponse(success=True, data=current_user)
