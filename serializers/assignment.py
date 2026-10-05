from pydantic import BaseModel
from typing import Optional
from datetime import date


class AssignmentSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    course_id: int

    class Config:
        from_attributes = True


class CreateAssignmentSchema(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None


class UpdateAssignmentSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None