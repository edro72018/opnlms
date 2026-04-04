from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db, get_current_user
from app.schemas.enrollment import (
    EnrollmentResponse,
    EnrollmentWithCourseResponse,
    StudentInCourseResponse,
)
from app.schemas.base import APIResponse
from app.schemas.user import UserResponse
from app.services.enrollment import EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["inscripciones"])


@router.post("/{course_id}", response_model=APIResponse[EnrollmentResponse])
async def enroll(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = EnrollmentService(db)
    enrollment = await service.enroll(course_id, current_user)
    return APIResponse(
        success=True,
        data=enrollment,
        message="Inscripción exitosa",
    )


@router.delete("/{course_id}", response_model=APIResponse)
async def cancel_enrollment(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = EnrollmentService(db)
    await service.cancel(course_id, current_user)
    return APIResponse(success=True, message="Inscripción cancelada")


@router.get(
    "/my-courses", response_model=APIResponse[list[EnrollmentWithCourseResponse]]
)
async def my_courses(
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = EnrollmentService(db)
    enrollments = await service.my_courses(current_user)
    data = [EnrollmentWithCourseResponse.model_validate(e) for e in enrollments]
    return APIResponse(success=True, data=data)


@router.get(
    "/{course_id}/students", response_model=APIResponse[list[StudentInCourseResponse]]
)
async def students_in_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    service = EnrollmentService(db)
    students = await service.students_in_course(course_id, current_user)
    return APIResponse(success=True, data=students)
