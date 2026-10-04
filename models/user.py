from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from config.environment import JWT_SECRET

# role model 
from .role import UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)  # Each username must be unique
    email = Column(String, unique=True)  # Each email must be unique
    password = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole, name="user_role"), nullable=True , default=UserRole.STUDENT)

     # A user can teach many courses (as an instructor)...
    courses_taught = relationship(
        "CourseModel", back_populates="instructor", cascade="all, delete-orphan"
    )
    # ...and/or enroll in many courses (as a student)
    enrollments = relationship(
        "EnrollmentModel", back_populates="student", cascade="all, delete-orphan"
    )
    
    def set_password(self, plain_txt_password: str):
        self.password = pwd_context.hash(plain_txt_password)

    def verify_password(self, plain_txt_password: str) -> bool:
        return pwd_context.verify(plain_txt_password, self.password)

    def generate_token(self):
        payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=1),  # Expiration time (1 day)
        "iat": datetime.now(timezone.utc),  # Issued at time
        "sub": str(self.id),  # Subject - the user ID
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token