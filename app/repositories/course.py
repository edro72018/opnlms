from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.course import Course, Module
from uuid import UUID


class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Course]:
        result = await self.db.execute(
            select(Course).options(selectinload(Course.modules))
        )
        return result.scalars().all()

    async def get_by_id(self, course_id: UUID) -> Course | None:
        result = await self.db.execute(
            select(Course)
            .where(Course.id == course_id)
            .options(selectinload(Course.modules))
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Course:
        course = Course(**kwargs)
        self.db.add(course)
        await self.db.flush()
        await self.db.refresh(course, ["modules"])
        return course

    async def update(self, course: Course, **kwargs) -> Course:
        for field, value in kwargs.items():
            if value is not None:
                setattr(course, field, value)
        await self.db.flush()
        await self.db.refresh(course, ["modules"])
        return course

    async def delete(self, course: Course) -> None:
        await self.db.delete(course)
        await self.db.flush()

    async def create_module(self, **kwargs) -> Module:
        module = Module(**kwargs)
        self.db.add(module)
        await self.db.flush()
        await self.db.refresh(module)
        return module

    async def get_modules(self, course_id: UUID) -> list[Module]:
        result = await self.db.execute(
            select(Module).where(Module.course_id == course_id).order_by(Module.order)
        )
        return result.scalars().all()
