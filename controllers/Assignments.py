from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import UserModel
from models.course import CourseModel
from models.assignment import AssignmentModel
from models.enrollment import EnrollmentModel
from models.role import UserRole

# serializers
from serializers.assignment import ( AssignmentSchema,CreateAssignmentSchema,UpdateAssignmentSchema )

# dependencies 
from dependencies.get_current_user import get_current_user


router = APIRouter()


@router.get("/courses/{course_id}/assignments" , response_model=List[AssignmentSchema])
def getAssignments (
     course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    course=db.query(CourseModel).filter(CourseModel.id==course_id).first()
    if not course:
        raise HTTPException(status_code=404 , detail="Course not found")
    is_instructor = course.instructor_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    is_enrolled = (
        db.query(EnrollmentModel)
        .filter(
            EnrollmentModel.course_id == course_id,
            EnrollmentModel.student_id == current_user.id,
        )
        .first()
        is not None
    )

    if not (is_instructor or is_admin or is_enrolled):
        raise HTTPException(
            status_code=403, detail="You don't have access to this course's assignments"
        )

    return db.query(AssignmentModel).filter(AssignmentModel.course_id == course_id).all()


@router.post(
    "/courses/{course_id}/assignments", response_model=AssignmentSchema, status_code=201
)
def create_assignment(
    course_id: int,
    assignment: CreateAssignmentSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to add assignments to this course",
        )

    new_assignment = AssignmentModel(**assignment.dict(), course_id=course_id)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment


@router.put("/assignments/{assignment_id}", response_model=AssignmentSchema)
def update_assignment(
    assignment_id: int,
    assignment: UpdateAssignmentSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_assignment = (
        db.query(AssignmentModel).filter(AssignmentModel.id == assignment_id).first()
    )
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    course = db_assignment.course
    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="You don't have permission to edit this assignment"
        )

    for key, value in assignment.dict(exclude_unset=True).items():
        setattr(db_assignment, key, value)

    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.delete("/assignments/{assignment_id}", status_code=204)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_assignment = (
        db.query(AssignmentModel).filter(AssignmentModel.id == assignment_id).first()
    )
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    course = db_assignment.course
    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this assignment"
        )

    db.delete(db_assignment)
    db.commit()
    return None



 




