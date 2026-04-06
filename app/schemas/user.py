from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str | None = None
    last_name: str
    second_last_name: str | None = None
    password: str
    role: UserRole = UserRole.student

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("El password debe tener al menos 8 caracteres")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    middle_name: str | None
    last_name: str
    second_last_name: str | None
    full_name: str  # viene de la @property del modelo
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
