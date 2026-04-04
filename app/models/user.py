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

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        SAEnum(UserRole, name="userrole"),
        nullable=False,
        default=UserRole.student,
    )
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"
