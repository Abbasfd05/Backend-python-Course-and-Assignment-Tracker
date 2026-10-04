from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class CourseModel(BaseModel):

    title=Column(String, nullable=False)
    description=Column(String, nullable=False)
    semester=Column(String,nullable=False)
    instructor_id=Column(Integer, ForeignKey("users.id"), nullable=False)

    
    



