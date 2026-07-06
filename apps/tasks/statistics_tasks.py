from celery import shared_task

from apps.models import Course, Enrollment


@shared_task
def update_course_statistics():

    print("=" * 60)
    print("UPDATE COURSE STATISTICS")
    print("=" * 60)

    for course in Course.objects.all():

        total = Enrollment.objects.filter(
            course=course
        ).count()

        print(
            f"{course.title} -> {total} enrollment(s)"
        )

    print("=" * 60)

    return True