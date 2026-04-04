from unittest import result

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.course import Course
from uuid import UUID


class EnrollmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_student_and_course(
        self, student_id: UUID, course_id: UUID
    ) -> Enrollment | None:
        result = await self.db.execute(
            select(Enrollment).where(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_my_courses(self, student_id: UUID) -> list[Enrollment]:
        result = await self.db.execute(
            select(Enrollment)
            .where(
                Enrollment.student_id == student_id,
                Enrollment.is_active == True,
            )
            .options(selectinload(Enrollment.course).selectinload(Course.modules))
        )
        return result.scalars().all()

    async def get_students_in_course(self, course_id: UUID) -> list[Enrollment]:
        result = await self.db.execute(
            select(Enrollment)
            .where(
                Enrollment.course_id == course_id,
                Enrollment.is_active == True,
            )
            .options(selectinload(Enrollment.student))
        )
        return result.scalars().all()

    async def create(self, student_id: UUID, course_id: UUID) -> Enrollment:
        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
        )
        self.db.add(enrollment)
        await self.db.flush()
        await self.db.refresh(enrollment)
        return enrollment

    async def deactivate(self, enrollment: Enrollment) -> None:
        enrollment.is_active = False
        await self.db.flush()
