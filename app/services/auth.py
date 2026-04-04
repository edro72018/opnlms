from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import AuthError, LMSException


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> TokenResponse:
        # Verifica que el email no esté en uso
        if await self.repo.email_exists(data.email):
            raise LMSException("Este email ya está registrado", 409)

        # Crea el usuario — nunca guardamos el password en texto plano
        user = await self.repo.create(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            role=data.role,
        )

        return self._build_token_response(user)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)

        # Mismo mensaje si el email no existe o el password es incorrecto
        # Evitamos dar pistas sobre qué campo está mal (seguridad)
        if not user or not verify_password(data.password, user.hashed_password):
            raise AuthError("Email o password incorrectos")

        if not user.is_active:
            raise AuthError("Usuario inactivo. Contacta al administrador")

        return self._build_token_response(user)

    async def get_current_user(self, token: str) -> UserResponse:
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            raise AuthError("Token inválido o expirado")

        user = await self.repo.get_by_id(payload["sub"])
        if not user or not user.is_active:
            raise AuthError("Usuario no encontrado")

        return UserResponse.model_validate(user)

    def _build_token_response(self, user) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
            user=UserResponse.model_validate(user),
        )
