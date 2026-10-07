from models.user import UserModel
from models.role import UserRole

def create_test_users():
    admin = UserModel(username="Ahmed_Abbas", email="arjun@devmail.in" , role=UserRole.ADMIN)
    admin.set_password("123")
    student1 = UserModel(username="Ali_Ahmed", email="emma.johnson@email.com" , role=UserRole.STUDENT)
    student1.set_password("123")
    student2 = UserModel(username="fatima_ali", email="fatima.ali@mail.ae", role=UserRole.STUDENT)
    student2.set_password("123")
    instructor = UserModel(username="Prof.Mohammed", email="lucas.silva@correo.br", role=UserRole.INSTRUCTOR)
    instructor.set_password("123")
    student3 = UserModel(username="Denis", email="elena.popov@mail.ru", role=UserRole.STUDENT)
    student3.set_password("123")

    return [admin, student1, student2, instructor, student3]

user_list = create_test_users()