from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.repositories.enrollment import EnrollmentRepository
from app.repositories.course import CourseRepository
from app.schemas.user import UserResponse
from app.schemas.enrollment import StudentInCourseResponse
from app.models.user import UserRole
from app.core.exceptions import LMSException, NotFoundError, ForbiddenError


class EnrollmentService:
    def __init__(self, db: AsyncSession):
        self.repo = EnrollmentRepository(db)
        self.course_repo = CourseRepository(db)

    async def enroll(self, course_id: UUID, current_user: UserResponse):
        # Solo estudiantes pueden inscribirse
        if current_user.role != UserRole.student:
            raise ForbiddenError()

        # Verificar que el curso existe
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Curso")

        # Verificar que no esté ya inscrito
        existing = await self.repo.get_by_student_and_course(current_user.id, course_id)
        if existing:
            if existing.is_active:
                raise LMSException("Ya estás inscrito en este curso", 409)
            else:
                # Reactivar inscripción cancelada anteriormente
                existing.is_active = True
                return existing

        return await self.repo.create(current_user.id, course_id)

    async def cancel(self, course_id: UUID, current_user: UserResponse):
        enrollment = await self.repo.get_by_student_and_course(
            current_user.id, course_id
        )
        if not enrollment or not enrollment.is_active:
            raise NotFoundError("Inscripción")

        await self.repo.deactivate(enrollment)

    async def my_courses(self, current_user: UserResponse):
        if current_user.role != UserRole.student:
            raise ForbiddenError()
        return await self.repo.get_my_courses(current_user.id)

    async def students_in_course(
        self, course_id: UUID, current_user: UserResponse
    ) -> list[StudentInCourseResponse]:
        # Solo teacher y admin pueden ver la lista de estudiantes
        if current_user.role == UserRole.student:
            raise ForbiddenError()

        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Curso")

        enrollments = await self.repo.get_students_in_course(course_id)

        return [
            StudentInCourseResponse(
                enrollment_id=e.id,
                student_id=e.student.id,
                student_name=e.student.full_name,
                student_email=e.student.email,
                progress=e.progress,
                completed=e.completed,
            )
            for e in enrollments
        ]
