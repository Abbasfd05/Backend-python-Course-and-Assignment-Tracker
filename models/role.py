import enum 

class UserRole(str, enum.Enum): # Enum is SQLAlchemy's own column type and enum is Python's built-in
    STUDENT="student"
    INSTRUCTOR="instructor"
    ADMIN="admin"
