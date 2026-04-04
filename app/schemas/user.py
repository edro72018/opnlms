from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from app.models.user import UserRole


class RegisterRequest(BaseModel):
    """Lo que el cliente manda para registrarse."""

    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.student

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("El password debe tener al menos 8 caracteres")
        return v

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class LoginRequest(BaseModel):
    """Lo que el cliente manda para iniciar sesión."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Lo que el servidor devuelve sobre un usuario. Nunca incluye el password."""

    id: UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Los tokens que recibe el cliente al autenticarse."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
