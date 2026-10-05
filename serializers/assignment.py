
from pydantic import BaseModel
from typing import Optional
from datetime import date

class AssignmentSchema():
      id: int
      title: str 
      description: Optional[str]= None
      due_date: Optional[str]= None 
      course_id= int 

      class Config:
       from_attributes = True

        

class CreateAssignmentSchema():
       title: str 
       description: Optional[str]= None
       due_date: Optional[str]= None 
       

class UpdateAssignmentSchema():
    title: Optional[str]=None 
    description: Optional[str]= None
    due_date: Optional[str]= None 
    
        
    
