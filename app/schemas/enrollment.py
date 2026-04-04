from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.schemas.course import CourseResponse


class EnrollmentResponse(BaseModel):
    id: UUID
    student_id: UUID
    course_id: UUID
    progress: float
    is_active: bool
    completed: bool

    model_config = {"from_attributes": True}


class EnrollmentWithCourseResponse(BaseModel):
    id: UUID
    progress: float
    is_active: bool
    completed: bool
    course: CourseResponse

    model_config = {"from_attributes": True}


class StudentInCourseResponse(BaseModel):
    enrollment_id: UUID
    student_id: UUID
    student_name: str
    student_email: str
    progress: float
    completed: bool
