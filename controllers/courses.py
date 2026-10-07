
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import UserModel
from models.course import CourseModel
from models.enrollment import EnrollmentModel
from models.role import UserRole

# serializers
from serializers.course import CreateCourseSchema,CourseSchema,UpdateCourseSchema
from serializers.enrollment import StudentSummarySchema

# dependencies 
from dependencies.get_current_user import get_current_user
from dependencies.require_role import require_role

router = APIRouter()


@router.get("/courses", response_model=List[CourseSchema])
def get_courses(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Scope the list by role: admins see everything, instructors see what
    # they teach, students see only what they're enrolled in.
    if current_user.role == UserRole.ADMIN:
        return db.query(CourseModel).all()

    if current_user.role == UserRole.INSTRUCTOR:
        return (
            db.query(CourseModel)
            .filter(CourseModel.instructor_id == current_user.id)
            .all()
        )

    return (
        db.query(CourseModel)
        .join(EnrollmentModel, EnrollmentModel.course_id == CourseModel.id)
        .filter(EnrollmentModel.student_id == current_user.id)
        .all()
    )

@router.get("/courses/available", response_model=List[CourseSchema])
def get_available_courses(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Any authenticated user can browse every course, regardless of role.
    return db.query(CourseModel).all()


@router.get("/courses/{course_id}", response_model=CourseSchema)
def get_single_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/courses", response_model=CourseSchema, status_code=201)
def create_course(
    course: CreateCourseSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.INSTRUCTOR, UserRole.ADMIN)),
):
    new_course = CourseModel(**course.dict(), instructor_id=current_user.id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.put("/courses/{course_id}", response_model=CourseSchema)
def update_course(
    course_id: int,
    course: UpdateCourseSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    if db_course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="You don't have permission to edit this course"
        )

    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)

    db.commit()
    db.refresh(db_course)
    return db_course


@router.delete("/courses/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    if db_course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this course"
        )

    db.delete(db_course)
    db.commit()
    return None


@router.post("/courses/{course_id}/enroll", response_model=CourseSchema, status_code=201)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.STUDENT)),
):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = (
        db.query(EnrollmentModel)
        .filter(
            EnrollmentModel.course_id == course_id,
            EnrollmentModel.student_id == current_user.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Already enrolled in this course")

    db.add(EnrollmentModel(course_id=course_id, student_id=current_user.id))
    db.commit()
    return course


@router.delete("/courses/{course_id}/enroll", status_code=204)
def unenroll_from_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.STUDENT)),
):
    enrollment = (
        db.query(EnrollmentModel)
        .filter(
            EnrollmentModel.course_id == course_id,
            EnrollmentModel.student_id == current_user.id,
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="You are not enrolled in this course")

    db.delete(enrollment)
    db.commit()
    return None


@router.get("/courses/{course_id}/students", response_model=List[StudentSummarySchema])
def get_enrolled_students(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this course's students",
        )

    return [enrollment.student for enrollment in course.enrollments]
