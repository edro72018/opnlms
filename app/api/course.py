from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db, get_current_user
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    ModuleCreate,
    ModuleResponse,
)
from app.schemas.base import APIResponse
from app.schemas.user import UserResponse
from app.services.course import CourseService

router = APIRouter(prefix="/courses", tags=["cursos"])


@router.get("", response_model=APIResponse[list[CourseResponse]])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    courses = await service.get_all()
    return APIResponse(success=True, data=courses)


@router.post("", response_model=APIResponse[CourseResponse])
async def create_course(
    data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    course = await service.create(data, current_user)
    return APIResponse(success=True, data=course, message="Curso creado exitosamente")


@router.get("/{course_id}", response_model=APIResponse[CourseResponse])
async def get_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    course = await service.get_by_id(course_id)
    return APIResponse(success=True, data=course)


@router.put("/{course_id}", response_model=APIResponse[CourseResponse])
async def update_course(
    course_id: UUID,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    course = await service.update(course_id, data, current_user)
    return APIResponse(success=True, data=course, message="Curso actualizado")


@router.delete("/{course_id}", response_model=APIResponse)
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    await service.delete(course_id, current_user)
    return APIResponse(success=True, message="Curso eliminado")


@router.post("/{course_id}/modules", response_model=APIResponse[ModuleResponse])
async def create_module(
    course_id: UUID,
    data: ModuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    module = await service.create_module(course_id, data, current_user)
    return APIResponse(success=True, data=module, message="Módulo creado exitosamente")


@router.get("/{course_id}/modules", response_model=APIResponse[list[ModuleResponse]])
async def list_modules(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = CourseService(db)
    modules = await service.get_modules(course_id)
    return APIResponse(success=True, data=modules)
