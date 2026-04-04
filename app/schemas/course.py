from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.models.course import CourseStatus


class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0
    is_visible: bool = True


class ModuleResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    order: int
    is_visible: bool
    course_id: UUID

    model_config = {"from_attributes": True}


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: CourseStatus = CourseStatus.draft
    thumbnail_url: Optional[str] = None


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CourseStatus] = None
    thumbnail_url: Optional[str] = None


class CourseResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: CourseStatus
    thumbnail_url: Optional[str]
    created_by: Optional[UUID]
    modules: list[ModuleResponse] = []

    model_config = {"from_attributes": True}
