from ninja import Router
from django.shortcuts import get_object_or_404
from apps.mongodb.logger import log_activity
from apps.mongodb.analytics import update_learning_analytics
from apps.tasks.email_tasks import send_enrollment_email
from apps.tasks.certificate_tasks import generate_certificate

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

    if created:

        log_activity(
            user=request.auth,
            action="ENROLL_COURSE",
            detail={
                "course_id": course.id,
                "course_title": course.title
            }
        )

        send_enrollment_email.delay(
            request.auth.username,
            course.title
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
    
    total_lessons = Lesson.objects.filter(
        course=enrollment.course
    ).count()

    completed_lessons = Progress.objects.filter(
        enrollment=enrollment,
        completed=True
    ).count()

    if total_lessons > 0 and completed_lessons == total_lessons:

        generate_certificate.delay(
            enrollment.student.username,
            enrollment.course.title
        )

    update_learning_analytics(enrollment)

    log_activity(
        user=request.auth,
        action="COMPLETE_LESSON",
        detail={
            "course_id": enrollment.course.id,
            "course_title": enrollment.course.title,
            "lesson_id": lesson.id,
            "lesson_title": lesson.title
        }
    )

    return progress

