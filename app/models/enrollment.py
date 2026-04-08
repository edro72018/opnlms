from sqlalchemy import Column, Float, Boolean, ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
import uuid


class Enrollment(Base, TimestampMixin):
    __tablename__ = "enrollments"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    course_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )

    progress = Column(Float, default=0.0, nullable=False)  # 0.0 a 100.0
    is_active = Column(Boolean, default=True, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    # Relaciones
    student = relationship("User", foreign_keys=[student_id])
    course = relationship("Course", foreign_keys=[course_id])

    # Un estudiante no puede inscribirse dos veces al mismo curso
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

    def __repr__(self):
        return f"<Enrollment student={self.student_id} course={self.course_id} progress={self.progress}%>"
