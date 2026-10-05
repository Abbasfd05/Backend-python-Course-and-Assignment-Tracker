from pydantic import BaseModel
from typing import Optional


class CourseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    semester: Optional[str] = None
    instructor_id: int

    class Config:
        from_attributes = True


class CreateCourseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    semester: Optional[str] = None


class UpdateCourseSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    semester: Optional[str] = None