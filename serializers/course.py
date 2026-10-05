from click import Option
from pydantic import BaseModel
from typing import Optional
from datetime import date


class CourseSchema():
      id: int
      title: str 
      description: Optional[str]= None
      semester: Option[str]= None 
      instructor_id= int 

      class Config:
       from_attributes = True

        

class CreateCourseSchema():
       id: int
       description: Optional[str]= None
       semester: Option[str]= None 
       

class UpdateCourseSchema():
    title: Optional[str] = None
    description: Optional[str] = None
    semester: Optional[str] = None
        
    
