from sqlalchemy import Column, String, Boolean, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, TimestampMixin
import uuid
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)  # segundo nombre, opcional
    third_name = Column(String(100), nullable=True)  # tercer nombre, opcional
    last_name = Column(String(100), nullable=False)
    second_last_name = Column(String(100), nullable=True)  # segundo apellido, opcional
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        SAEnum(UserRole, name="userrole"),
        nullable=False,
        default=UserRole.student,
    )
    is_active = Column(Boolean, default=True, nullable=False)

    @property
    def full_name(self) -> str:
        """Construye el nombre completo dinámicamente."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.second_last_name:
            parts.append(self.second_last_name)
        return " ".join(parts)

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"
