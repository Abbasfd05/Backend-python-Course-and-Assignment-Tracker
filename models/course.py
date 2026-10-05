from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class CourseModel(BaseModel):

    __tablename__ = "courses"

    title=Column(String, nullable=False)
    description=Column(String, nullable=False)
    semester=Column(String,nullable=False)
    instructor_id=Column(Integer, ForeignKey("users.id"), nullable=False)

    instructor = relationship("UserModel", back_populates="courses_taught")
    assignments = relationship(
        "AssignmentModel", back_populates="course", cascade="all, delete-orphan"
    )
    enrollments = relationship(
        "EnrollmentModel", back_populates="course", cascade="all, delete-orphan"
        # use all to propagate every operation in SQLAlchemy, without it we have to manually manage related rows every time
        # delete-orphan means if a child loses the parent, then it should be deleted. So, here if a course is deleted, then the student will also be deleted.
    )
    



