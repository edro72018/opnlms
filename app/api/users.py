from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db, get_current_user
from app.schemas.user import UserResponse, UserUpdate, UserUpdateMe
from app.schemas.base import APIResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["usuarios"])


@router.get("", response_model=APIResponse[list[UserResponse]])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = UserService(db)
    usuarios = await service.get_all(current_user)
    return APIResponse(success=True, data=usuarios)


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return APIResponse(success=True, data=current_user)


@router.patch("/me", response_model=APIResponse[UserResponse])
async def update_me(
    data: UserUpdateMe,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = UserService(db)
    usuario = await service.update_me(data, current_user)
    return APIResponse(success=True, data=usuario, message="Perfil actualizado")


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = UserService(db)
    usuario = await service.get_by_id(user_id, current_user)
    return APIResponse(success=True, data=usuario)


@router.put("/{user_id}", response_model=APIResponse[UserResponse])
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = UserService(db)
    usuario = await service.update(user_id, data, current_user)
    return APIResponse(success=True, data=usuario, message="Usuario actualizado")


@router.delete("/{user_id}", response_model=APIResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = UserService(db)
    await service.delete(user_id, current_user)
    return APIResponse(success=True, message="Usuario desactivado")
