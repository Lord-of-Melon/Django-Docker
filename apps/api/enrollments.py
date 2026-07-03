from ninja import Router
from django.shortcuts import get_object_or_404

from apps.models import (
    Course,
    Enrollment,
    Lesson,
    Progress,
)

from .schemas import (
    EnrollmentCreate,
    EnrollmentOut,
    ProgressCreate,
    ProgressOut,
)

from .security import JWTAuth
from .permissions import is_student

router = Router(tags=["Enrollments"])

@router.post("/", auth=JWTAuth(), response=EnrollmentOut)
def enroll(request, data: EnrollmentCreate):

    is_student(request.auth)

    course = get_object_or_404(
        Course,
        id=data.course_id
    )

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.auth,
        course=course
    )

    return enrollment
@router.get("/my-courses", auth=JWTAuth(), response=list[EnrollmentOut])
def my_courses(request):

    is_student(request.auth)

    return (
        Enrollment.objects
        .filter(student=request.auth)
        .select_related(
            "course",
            "course__category",
            "course__instructor"
        )
    )

from ninja.errors import HttpError

@router.post("/{enrollment_id}/progress", auth=JWTAuth(), response=ProgressOut)
def complete_lesson(
    request,
    enrollment_id: int,
    data: ProgressCreate
):

    is_student(request.auth)

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=request.auth
    )

    lesson = get_object_or_404(
        Lesson,
        id=data.lesson_id
    )

    # Validasi bahwa lesson milik course yang diikuti
    if lesson.course != enrollment.course:
        raise HttpError(
            400,
            "Lesson bukan milik course yang diikuti."
        )

    progress, created = Progress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    progress.completed = True
    progress.save()

    return progress

