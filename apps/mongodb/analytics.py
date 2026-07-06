from datetime import datetime

from apps.mongodb.client import db
from apps.models import Lesson, Progress


def update_learning_analytics(enrollment):
    """
    Update learning analytics untuk satu enrollment.
    """

    total_lessons = Lesson.objects.filter(
        course=enrollment.course
    ).count()

    completed_lessons = Progress.objects.filter(
        enrollment=enrollment,
        completed=True
    ).count()

    completion_rate = 0

    if total_lessons > 0:
        completion_rate = round(
            completed_lessons / total_lessons * 100,
            2
        )

    db.learning_analytics.update_one(
        {
            "enrollment_id": enrollment.id
        },
        {
            "$set": {
                "student_id": enrollment.student.id,
                "student_username": enrollment.student.username,
                "course_id": enrollment.course.id,
                "course_title": enrollment.course.title,
                "completed_lessons": completed_lessons,
                "total_lessons": total_lessons,
                "completion_rate": completion_rate,
                "last_activity": datetime.utcnow()
            }
        },
        upsert=True
    )