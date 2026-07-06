from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .rate_limit import rate_limit
from apps.mongodb.logger import log_activity

from apps.models import Course, Category
from .schemas import CourseOut, CourseCreate
from .security import JWTAuth
from .permissions import (
    is_admin,
    is_course_owner,
    is_instructor,
)

router = Router(tags=["Courses"])

# =========================
# Cache Keys
# =========================
COURSE_LIST_CACHE_KEY = "course_list"


def course_detail_cache_key(course_id: int):
    return f"course_{course_id}"


# =========================
# Public Endpoints
# =========================

@router.get("/", response=list[CourseOut])
def list_courses(request):

    rate_limit(request)
    courses = cache.get(COURSE_LIST_CACHE_KEY)

    if courses is None:
        print("CACHE MISS")

        courses = list(
            Course.objects.for_listing()
        )

        cache.set(
            COURSE_LIST_CACHE_KEY,
            courses,
            timeout=300
        )

    else:
        print("CACHE HIT")

    return courses


@router.get("/{course_id}", response=CourseOut)
def get_course(request, course_id: int):

    rate_limit(request)
    cache_key = course_detail_cache_key(course_id)
    course = cache.get(cache_key)

    if course is None:
        print("DETAIL CACHE MISS")

        course = get_object_or_404(
            Course.objects.for_listing(),
            id=course_id
        )

        cache.set(
            cache_key,
            course,
            timeout=300
        )

    else:
        print("DETAIL CACHE HIT")

    return course


# =========================
# Protected Endpoints
# =========================

@router.post("/", auth=JWTAuth(), response=CourseOut)
def create_course(request, data: CourseCreate):
    rate_limit(request)
    is_instructor(request.auth)

    category = get_object_or_404(
        Category,
        id=data.category_id
    )

    course = Course.objects.create(
        title=data.title,
        instructor=request.auth,
        category=category
    )

    log_activity(
    user=request.auth,
    action="CREATE_COURSE",
    detail={
        "course_id": course.id,
        "course_title": course.title,
        "category": category.name
    }
)
    # Hapus cache list
    cache.delete(COURSE_LIST_CACHE_KEY)

    return course


@router.patch("/{course_id}", auth=JWTAuth(), response=CourseOut)
def update_course(request, course_id: int, data: CourseCreate):
    rate_limit(request)
    course = get_object_or_404(
        Course,
        id=course_id
    )

    is_course_owner(request.auth, course)

    category = get_object_or_404(
        Category,
        id=data.category_id
    )

    course.title = data.title
    course.category = category
    course.save()

    log_activity(
    user=request.auth,
    action="UPDATE_COURSE",
    detail={
        "course_id": course.id,
        "course_title": course.title
    }
)

    # Hapus cache
    cache.delete(COURSE_LIST_CACHE_KEY)
    cache.delete(course_detail_cache_key(course.id))

    return course


@router.delete("/{course_id}", auth=JWTAuth())
def delete_course(request, course_id: int):
    rate_limit(request)
    is_admin(request.auth)

    course = get_object_or_404(
        Course,
        id=course_id
    )

    # Hapus cache sebelum delete
    cache.delete(COURSE_LIST_CACHE_KEY)
    cache.delete(course_detail_cache_key(course.id))

    course.delete()
    
    log_activity(
    user=request.auth,
    action="DELETE_COURSE",
    detail={
        "course_id": course.id,
        "course_title": course.title
    }
)

    return {
        "message": "Course berhasil dihapus."
    }