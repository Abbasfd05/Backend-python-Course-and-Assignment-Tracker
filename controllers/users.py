# controllers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.user import UserModel
from models.role import UserRole
from serializers.user import (
    UserSchema,
    UserRegistrationSchema,
    UserLoginSchema,
    UserTokenSchema,
    UserRoleUpdateSchema,
)
from database import get_db
from dependencies.get_current_user import get_current_user
from dependencies.require_role import require_role
router = APIRouter()

@router.post("/register", response_model=UserTokenSchema, status_code=201)
def create_user(user: UserRegistrationSchema, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    # Initialize the user class (instance)
    new_user = UserModel(username=user.username, email=user.email)
    # Use the set_password method to hash the password
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token = new_user.generate_token()

        # Return token and a success message
    return {"token": token, "message": "Login successful"}

@router.post("/login", response_model=UserTokenSchema, status_code=201)
def login(user: UserLoginSchema, db: Session = Depends(get_db)):

    # Find the user by username
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    # Check if the user exists and if the password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=409, detail="Invalid username or password")

    # Generate JWT token
    token = db_user.generate_token()

    # Return token and a success message
    return {"token": token, "message": "Login successful"}

@router.get('/current_user', response_model=UserSchema)
def current_user(user: UserSchema = Depends(get_current_user)):
    return user



@router.get("/users", response_model=List[UserSchema])
def get_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.ADMIN)),
):
    return db.query(UserModel).all()


@router.put("/users/{user_id}", response_model=UserSchema)
def update_user_role(
    user_id: int,
    payload: UserRoleUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.ADMIN)),
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = payload.role
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.ADMIN)),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
