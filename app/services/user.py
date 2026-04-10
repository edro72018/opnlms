from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse, UserUpdate, UserUpdateMe
from app.core.exceptions import NotFoundError, ForbiddenError
from app.core.security import hash_password
from app.models.user import UserRole


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_all(self, current_user: UserResponse) -> list[UserResponse]:
        if current_user.role != UserRole.admin:
            raise ForbiddenError()
        usuarios = await self.repo.get_all()
        return [UserResponse.model_validate(u) for u in usuarios]

    async def get_by_id(self, user_id: UUID, current_user: UserResponse) -> UserResponse:
        # Admin ve a cualquiera; los demás solo a sí mismos
        if current_user.role != UserRole.admin and current_user.id != user_id:
            raise ForbiddenError()
        usuario = await self.repo.get_by_id(user_id)
        if not usuario:
            raise NotFoundError("Usuario")
        return UserResponse.model_validate(usuario)

    async def update(self, user_id: UUID, data: UserUpdate, current_user: UserResponse) -> UserResponse:
        if current_user.role != UserRole.admin:
            raise ForbiddenError()
        usuario = await self.repo.get_by_id(user_id)
        if not usuario:
            raise NotFoundError("Usuario")
        cambios = data.model_dump(exclude_none=True)
        usuario = await self.repo.update(usuario, **cambios)
        return UserResponse.model_validate(usuario)

    async def update_me(self, data: UserUpdateMe, current_user: UserResponse) -> UserResponse:
        usuario = await self.repo.get_by_id(current_user.id)
        if not usuario:
            raise NotFoundError("Usuario")
        cambios = data.model_dump(exclude_none=True)
        if "password" in cambios:
            cambios["hashed_password"] = hash_password(cambios.pop("password"))
        usuario = await self.repo.update(usuario, **cambios)
        return UserResponse.model_validate(usuario)

    async def delete(self, user_id: UUID, current_user: UserResponse) -> None:
        if current_user.role != UserRole.admin:
            raise ForbiddenError()
        usuario = await self.repo.get_by_id(user_id)
        if not usuario:
            raise NotFoundError("Usuario")
        await self.repo.update(usuario, is_active=False)
