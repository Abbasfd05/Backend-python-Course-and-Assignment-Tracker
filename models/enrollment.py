from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class EnrollmentModel(BaseModel):

    student_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id=Column(Integer, ForeignKey("courses.id"), nullable=False)

    student = relationship("UserModel", back_populates="enrollments")
    course = relationship("CourseModel", back_populates="enrollments")
