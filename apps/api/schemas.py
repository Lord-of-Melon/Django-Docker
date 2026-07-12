from ninja import Schema
from datetime import datetime
from pydantic import Field

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
    level: str = "beginner"

class CourseOut(Schema):
    id: int
    title: str
    instructor: UserOut
    category: CategoryOut | None

    level: str
    status: str

    student_count: int
    average_rating: float

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

class ReviewOut(Schema):
    id: int
    rating: int
    review: str

    student: UserOut

    created_at: datetime

class WishlistOut(Schema):

    id: int

    course: CourseOut

    created_at: datetime

class DashboardOut(Schema):

    active_courses: int

    completed_courses: int

    wishlist_count: int

    recommendation_count: int

    overall_progress: int

    active_course_list: list[CourseOut]

    recommendations: list[CourseOut]

class CourseFilter(Schema):

    keyword: str | None = None

    category: int | None = None

    instructor: int | None = None

    level: str | None = None

    status: str | None = None

    ordering: str | None = None

class ReviewCreate(Schema):

    rating: int = Field(
        ge=1,
        le=10
    )

    review: str = Field(
        min_length=5,
        max_length=500
    )
