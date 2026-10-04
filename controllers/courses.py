
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import UserModel
from models.course import CourseModel
from models.enrollment import EnrollmentModel
from models.role import UserRole

# serializers


# dependencies 
from dependencies.get_current_user import get_current_user
from dependencies.require_role import require_role

router = APIRouter()