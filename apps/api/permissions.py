from ninja.errors import HttpError
from apps.models import Course


def is_admin(user):
    if user.role != "admin":
        raise HttpError(403, "Hanya Admin yang dapat mengakses endpoint ini.")


def is_instructor(user):
    if user.role != "instructor":
        raise HttpError(403, "Hanya Instructor yang dapat mengakses endpoint ini.")


def is_student(user):
    if user.role != "student":
        raise HttpError(403, "Hanya Student yang dapat mengakses endpoint ini.")
    

def is_course_owner(user, course: Course):
    if course.instructor != user:
        raise HttpError(
            403,
            "Anda bukan pemilik course ini."
        )