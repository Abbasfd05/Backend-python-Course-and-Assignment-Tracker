from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import UserModel
from models.role import UserRole
from tests.lib import login


def make_user(test_db: Session, username, email, role, password="mys3cretp2ssw0rd"):
    user = UserModel(username=username, email=email, role=role)
    user.set_password(password)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


def test_instructor_can_create_course(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    instructor = make_user(test_db, "courseInstructor1", "instructor1@example.com", UserRole.INSTRUCTOR)
    headers = login(test_app, "courseInstructor1", "mys3cretp2ssw0rd")

    response = test_app.post(
        "/api/courses",
        headers=headers,
        json={"title": "Intro to Testing", "description": "Pytest basics", "semester": "Fall 2026"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Intro to Testing"
    assert data["instructor_id"] == instructor.id


def test_student_cannot_create_course(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    make_user(test_db, "courseStudent1", "student1@example.com", UserRole.STUDENT)
    headers = login(test_app, "courseStudent1", "mys3cretp2ssw0rd")

    response = test_app.post(
        "/api/courses",
        headers=headers,
        json={"title": "Should Fail", "description": "", "semester": "Fall 2026"},
    )

    assert response.status_code == 403


def test_student_can_enroll_and_view_assignments(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    instructor = make_user(test_db, "courseInstructor2", "instructor2@example.com", UserRole.INSTRUCTOR)
    student = make_user(test_db, "courseStudent2", "student2@example.com", UserRole.STUDENT)

    instructor_headers = login(test_app, "courseInstructor2", "mys3cretp2ssw0rd")
    student_headers = login(test_app, "courseStudent2", "mys3cretp2ssw0rd")

    # Instructor creates a course and an assignment inside it
    course_res = test_app.post(
        "/api/courses",
        headers=instructor_headers,
        json={"title": "Data Structures", "description": "", "semester": "Fall 2026"},
    )
    course_id = course_res.json()["id"]

    assignment_res = test_app.post(
        f"/api/courses/{course_id}/assignments",
        headers=instructor_headers,
        json={"title": "Linked Lists", "description": "Implement one", "due_date": "2026-11-01"},
    )
    assert assignment_res.status_code == 201

    # A student who isn't enrolled yet can't see assignments
    denied = test_app.get(f"/api/courses/{course_id}/assignments", headers=student_headers)
    assert denied.status_code == 403

    # Student enrolls, then can see the assignment
    enroll_res = test_app.post(f"/api/courses/{course_id}/enroll", headers=student_headers)
    assert enroll_res.status_code == 201

    assignments_res = test_app.get(f"/api/courses/{course_id}/assignments", headers=student_headers)
    assert assignments_res.status_code == 200
    titles = [a["title"] for a in assignments_res.json()]
    assert "Linked Lists" in titles


def test_admin_can_list_all_users(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    make_user(test_db, "courseAdmin1", "admin1@example.com", UserRole.ADMIN)
    headers = login(test_app, "courseAdmin1", "mys3cretp2ssw0rd")

    response = test_app.get("/api/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_non_admin_cannot_list_users(
    test_app: TestClient,
    test_db: Session,
    override_get_db,
):
    make_user(test_db, "courseStudent3", "student3@example.com", UserRole.STUDENT)
    headers = login(test_app, "courseStudent3", "mys3cretp2ssw0rd")

    response = test_app.get("/api/users", headers=headers)
    assert response.status_code == 403
