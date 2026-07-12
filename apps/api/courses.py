from unicodedata import category
from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .rate_limit import rate_limit
from apps.mongodb.logger import log_activity
from apps.utils.category import get_category_descendants
import hashlib

from apps.models import Course, Category
from .schemas import CourseOut, CourseCreate
from .security import JWTAuth
from .permissions import (
    is_admin,
    is_course_owner,
    is_instructor,
)

from django.db.models import Q

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
def list_courses(
    request,
    keyword: str | None = None,
    category: int | None = None,
    instructor: int | None = None,
    level: str | None = None,
    status: str | None = None,
    ordering: str | None = None,
):

    rate_limit(request)

    # Cache key berdasarkan parameter pencarian
    raw_key = (
        f"{keyword}|"
        f"{category}|"
        f"{instructor}|"
        f"{level}|"
        f"{status}|"
        f"{ordering}"
    )

    cache_key = (
        "course_list_"
        + hashlib.md5(
            raw_key.encode()
        ).hexdigest()
    )

    courses = cache.get(cache_key)

    if courses is None:

        print("CACHE MISS")

        queryset = Course.objects.for_listing()

        # ======================
        # Search
        # ======================

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(category__name__icontains=keyword)
                | Q(instructor__username__icontains=keyword)
            )

        # ======================
        # Filter
        # ======================

        if category:
            category_ids = get_category_descendants(category)

            queryset = queryset.filter(
                category_id__in=category_ids
            )

        if instructor:
            queryset = queryset.filter(
                instructor_id=instructor
            )

        if level:
            queryset = queryset.filter(
                level=level
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        # ======================
        # Sorting
        # ======================

        if ordering == "title":
            queryset = queryset.order_by("title")

        elif ordering == "-title":
            queryset = queryset.order_by("-title")

        elif ordering == "rating":
            queryset = queryset.order_by("-average_rating")

        elif ordering == "popular":
            queryset = queryset.order_by("-student_count")

        courses = list(queryset)

        cache.set(
            cache_key,
            courses,
            timeout=300
        )

    else:

        print("CACHE HIT")

    user = getattr(request, "auth", None)

    log_activity(
        user=user,
        action="SEARCH_COURSE",
        detail={
            "keyword": keyword,
            "category": category,
            "instructor": instructor,
            "level": level,
            "status": status,
            "ordering": ordering,
        }
    )

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
        category=category,
        level=data.level
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
    cache.clear()

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
    course.level = data.level

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
    cache.clear()

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

    
    log_activity(
        user=request.auth,
        action="CREATE_COURSE",
        detail={
            "course_id": course.id,
            "course_title": course.title,
            "category": category.name
        }
    )
    course.delete()
    cache.clear()

    return {
        "message": "Course berhasil dihapus."
    }

