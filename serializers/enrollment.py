from pydantic import BaseModel


class EnrollmentSchema(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True


class StudentSummarySchema(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
