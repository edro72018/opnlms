from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from app.models.user import UserRole, UserSex


class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str | None = None
    last_name: str
    second_last_name: str | None = None
    password: str
    sex: UserSex | None = None

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
    sex: UserSex | None
    is_active: bool

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Admin: puede editar cualquier usuario."""
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    second_last_name: str | None = None
    sex: UserSex | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserUpdateMe(BaseModel):
    """El propio usuario edita su perfil (sin poder cambiar rol ni is_active)."""
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    second_last_name: str | None = None
    sex: UserSex | None = None
    password: str | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError("El password debe tener al menos 8 caracteres")
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
