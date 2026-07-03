from ninja import Schema
from datetime import datetime

class UserOut(Schema):
    id: int
    username: str
    email: str
    role: str

class RegisterSchema(Schema):
    username: str
    email: str
    password: str

class LoginSchema(Schema):
    username: str
    password: str

class CategoryOut(Schema):
    id: int
    name: str

class CourseCreate(Schema):
    title: str
    category_id: int

class CourseOut(Schema):
    id: int
    title: str
    instructor: UserOut
    category: CategoryOut | None

class LessonOut(Schema):
    id: int
    title: str
    order: int

class EnrollmentCreate(Schema):
    course_id: int

class EnrollmentOut(Schema):
    id: int
    student: UserOut
    course: CourseOut
    enrolled_at: datetime

class ProgressCreate(Schema):
    lesson_id: int

class ProgressOut(Schema):
    id: int
    lesson: LessonOut
    completed: bool

class TokenOut(Schema):
    access: str
    refresh: str

class RefreshSchema(Schema):
    refresh: str

class AccessTokenOut(Schema):
    access: str

class UpdateProfileSchema(Schema):
    username: str
    email: str

class CourseCreate(Schema):
    title: str
    category_id: int

class EnrollmentCreate(Schema):
    course_id: int

class EnrollmentOut(Schema):
    id: int
    course: CourseOut
    enrolled_at: datetime

