from ninja import Router
from django.db.models import Count, Avg
from django.core.cache import cache
from django.db.models import F, FloatField, ExpressionWrapper

from apps.models import (
    Enrollment,
    Wishlist,
    Course,
)
from apps.mongodb.logger import log_activity

from .schemas import DashboardOut
from .security import JWTAuth
from .permissions import is_student

router = Router(tags=["Dashboard"])

def dashboard_cache_key(user_id):

    return f"dashboard_{user_id}"

def calculate_progress(enrollment):

    total = enrollment.course.lessons.count()

    if total == 0:
        return 0

    completed = (
        enrollment.progress_set
        .filter(completed=True)
        .count()
    )

    return int(
        completed * 100 / total
    )
@router.get(
    "/",
    auth=JWTAuth(),
    response=DashboardOut
)
def dashboard(request):

    is_student(request.auth)

    cache_key = dashboard_cache_key(
        request.auth.id
    )

    data = cache.get(cache_key)

    if data:

        return data
    
    active_courses = (
        Enrollment.objects
        .filter(
            student=request.auth,
            status="active"
        )
        .select_related(
            "course",
            "course__category",
            "course__instructor"
        )
    )

    completed_courses = (
        Enrollment.objects.filter(
            student=request.auth,
            status="completed"
        ).count()
    )

    wishlist_count = (
        Wishlist.objects.filter(
            student=request.auth
        ).count()
    )

    progress_list = [
        calculate_progress(e)
        for e in active_courses
    ]

    overall_progress = (
        int(sum(progress_list) / len(progress_list))
        if progress_list
        else 0
    )

    category_ids = (
        active_courses
        .values_list(
            "course__category_id",
            flat=True
        )
        .distinct()
    )

    recommendations = (
        Course.objects.for_listing()
        .filter(
            category_id__in=category_ids
        )
        .exclude(
            enrollment__student=request.auth
        )
        .order_by(
            "-average_rating",
            "-student_count"
        )[:5]
    )   

    data = {

        "active_courses": active_courses.count(),

        "completed_courses": completed_courses,

        "wishlist_count": wishlist_count,

        "recommendation_count": len(recommendations),

        "overall_progress": overall_progress,

        "active_course_list": [
            e.course
            for e in active_courses
        ],

        "recommendations": recommendations

    }

    log_activity(

        user=request.auth,

        action="VIEW_DASHBOARD",

        detail={

            "active_courses": active_courses.count(),

            "completed_courses": completed_courses

        }

    )

    cache.set(
        cache_key,
        data,
        timeout=300
    )

    return data