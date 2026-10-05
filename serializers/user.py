# serializers/user.py

from pydantic import BaseModel
from models.role import UserRole

# Form Validations
class UserRegistrationSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str  # Plain text password for user registration (will be hashed before saving)

class UserLoginSchema(BaseModel):
    username: str  # User's unique name
    password: str  # Plain text password for user registration (will be hashed before saving)

class UserRoleUpdateSchema(BaseModel):
    role: UserRole

# Response Schemas
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True

class UserTokenSchema(BaseModel):
    token: str
    message: str
