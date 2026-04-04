from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate, ModuleCreate
from app.schemas.user import UserResponse
from app.models.user import UserRole
from app.core.exceptions import NotFoundError, ForbiddenError


class CourseService:
    def __init__(self, db: AsyncSession):
        self.repo = CourseRepository(db)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, course_id: UUID):
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Curso")
        return course

    async def create(self, data: CourseCreate, current_user: UserResponse):
        self._require_teacher_or_admin(current_user)
        return await self.repo.create(
            title=data.title,
            description=data.description,
            status=data.status,
            thumbnail_url=data.thumbnail_url,
            created_by=current_user.id,
        )

    async def update(
        self, course_id: UUID, data: CourseUpdate, current_user: UserResponse
    ):
        self._require_teacher_or_admin(current_user)
        course = await self.get_by_id(course_id)
        return await self.repo.update(
            course,
            title=data.title,
            description=data.description,
            status=data.status,
            thumbnail_url=data.thumbnail_url,
        )

    async def delete(self, course_id: UUID, current_user: UserResponse):
        # Solo admin puede eliminar
        if current_user.role != UserRole.admin:
            raise ForbiddenError()
        course = await self.get_by_id(course_id)
        await self.repo.delete(course)

    async def create_module(
        self, course_id: UUID, data: ModuleCreate, current_user: UserResponse
    ):
        self._require_teacher_or_admin(current_user)
        await self.get_by_id(course_id)  # verifica que el curso existe
        return await self.repo.create_module(
            title=data.title,
            description=data.description,
            order=data.order,
            is_visible=data.is_visible,
            course_id=course_id,
        )

    async def get_modules(self, course_id: UUID):
        await self.get_by_id(course_id)  # verifica que el curso existe
        return await self.repo.get_modules(course_id)

    def _require_teacher_or_admin(self, user: UserResponse):
        if user.role not in [UserRole.admin, UserRole.teacher]:
            raise ForbiddenError()
