# seed.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.environment import DATABASE_URL
from models.base import Base
from models.user import UserModel
from models.course import CourseModel
from models.assignment import AssignmentModel
from models.enrollment import EnrollmentModel

from data.user_data import user_list

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# This seed file is a separate program that can be used to "seed" our database with some initial data.
try:
    print("Recreating database...")
    # Dropping (or deleting) the tables and creating them again is for convenience. Once we start to play around with
    # our data, changing our models, this seed program will allow us to rapidly throw out the old data and replace it.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("seeding the database...")
    # Seed users: one admin, three students, and one instructor.
    db = SessionLocal()

    db.add_all(user_list)
    db.commit()
    for user in user_list:
        db.refresh(user)

    admin, student1, student2, instructor, student3 = user_list

     # Seed courses, which is owned by the one instructor
    course1 = CourseModel(
        title="Intro to Python",
        description="Fundamentals of Python programming",
        semester="Fall 2026",
        instructor_id=instructor.id,
    )
    course2 = CourseModel(
        title="Web Development",
        description="HTML, CSS, JavaScript and React basics",
        semester="Fall 2026",
        instructor_id=instructor.id,
    )
    db.add_all([course1, course2])
    db.commit()
    db.refresh(course1)
    db.refresh(course2)

    # Seed assignments, which belongs to those courses
    db.add_all([
        AssignmentModel(
            title="Variables and Loops",
            description="Practice basic syntax",
            due_date="2026-10-15",
            course_id=course1.id,
        ),
        AssignmentModel(
            title="Functions Lab",
            description="Write and test small functions",
            due_date="2026-10-22",
            course_id=course1.id,
        ),
        AssignmentModel(
            title="Build a Landing Page",
            description="HTML and CSS layout practice",
            due_date="2026-10-18",
            course_id=course2.id,
        ),
    ])

    # Seed enrollments that link students to courses
    db.add_all([
        EnrollmentModel(student_id=student1.id, course_id=course1.id),
        EnrollmentModel(student_id=student2.id, course_id=course1.id),
        EnrollmentModel(student_id=student1.id, course_id=course2.id),
        EnrollmentModel(student_id=student3.id, course_id=course2.id),
    ])

    db.commit()
    db.close()

    print("Database seeding complete! 👋")
except Exception as e:
    print("An error occurred:", e)