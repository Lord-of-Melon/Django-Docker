from ninja import Router
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.core.cache import cache

from apps.models import (
    Wishlist,
    Course,
    Enrollment,
)

from .schemas import (
    WishlistOut,
)

from .security import JWTAuth
from .permissions import is_student

from apps.mongodb.logger import log_activity

router = Router(tags=["Wishlist"])

@router.post(
    "/",
    auth=JWTAuth(),
    response=WishlistOut
)
def add_wishlist(
    request,
    course_id: int
):

    is_student(request.auth)

    course = get_object_or_404(
        Course,
        id=course_id
    )

    enrollment = Enrollment.objects.filter(
        student=request.auth,
        course=course
    ).first()

    if enrollment and enrollment.status == "completed":
        raise HttpError(
            400,
            "Course sudah selesai sehingga tidak dapat dimasukkan wishlist."
        )

    if Wishlist.objects.filter(
        student=request.auth,
        course=course
    ).exists():

        raise HttpError(
            400,
            "Course sudah ada di wishlist."
        )

    wishlist = Wishlist.objects.create(
        student=request.auth,
        course=course
    )

    cache.delete(f"dashboard_{request.auth.id}")

    log_activity(
        user=request.auth,
        action="ADD_WISHLIST",
        detail={
            "course_id": course.id,
            "course_title": course.title
        }
    )

    return wishlist

@router.get(
    "/",
    auth=JWTAuth(),
    response=list[WishlistOut]
)
def my_wishlist(request):

    is_student(request.auth)

    return (
        Wishlist.objects
        .filter(student=request.auth)
        .select_related(
            "course",
            "course__category",
            "course__instructor"
        )
        .order_by("-created_at")
    )

@router.delete(
    "/{wishlist_id}",
    auth=JWTAuth()
)
def delete_wishlist(
    request,
    wishlist_id: int
):

    is_student(request.auth)

    wishlist = get_object_or_404(
        Wishlist,
        id=wishlist_id
    )

    if wishlist.student != request.auth:
        raise HttpError(
            403,
            "Anda bukan pemilik wishlist ini."
        )

    course = wishlist.course

    wishlist.delete()

    cache.delete(f"dashboard_{request.auth.id}")

    log_activity(
        user=request.auth,
        action="DELETE_WISHLIST",
        detail={
            "course_id": course.id,
            "course_title": course.title
        }
    )

    return {
        "message": "Wishlist berhasil dihapus."
    }