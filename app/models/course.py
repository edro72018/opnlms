from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
import uuid
import enum


class CourseStatus(str, enum.Enum):
    draft = "draft"  # borrador, no visible para estudiantes
    published = "published"  # visible y accesible
    archived = "archived"  # ya no activo


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SAEnum(CourseStatus, name="coursestatus"),
        nullable=False,
        default=CourseStatus.draft,
    )
    thumbnail_url = Column(String(500), nullable=True)

    # Quién creó el curso
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relación con módulos
    modules = relationship(
        "Module",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.order",
    )

    def __repr__(self):
        return f"<Course {self.title} [{self.status}]>"


class Module(Base, TimestampMixin):
    __tablename__ = "modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)  # orden dentro del curso
    is_visible = Column(Boolean, default=True, nullable=False)

    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relación inversa
    course = relationship("Course", back_populates="modules")

    def __repr__(self):
        return f"<Module {self.title} [order={self.order}]>"
