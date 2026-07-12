
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from ninja.errors import HttpError

from apps.models import (
    Course,
    Review,
    Enrollment,
)

from .schemas import (
    ReviewCreate,
    ReviewOut,
)

from .security import JWTAuth
from .permissions import is_student

from apps.mongodb.logger import log_activity

from django.core.cache import cache


router = Router(tags=["Reviews"])

def update_course_average_rating(course):

    average = (
        Review.objects
        .filter(course=course)
        .aggregate(avg=Avg("rating"))
    )["avg"] or 0

    course.average_rating = average
    course.save(
        update_fields=["average_rating"]
    )

@router.post("/course/{course_id}", auth=JWTAuth(), response=ReviewOut)
def create_review(
    request,
    course_id: int,
    data: ReviewCreate
):

    is_student(request.auth)

    course = get_object_or_404(
        Course,
        id=course_id
    )

    enrolled = Enrollment.objects.filter(
        student=request.auth,
        course=course
    ).exists()

    if not enrolled:
        raise HttpError(
            403,
            "Anda belum mengikuti course ini."
        )
    if Review.objects.filter(
        student=request.auth,
        course=course
    ).exists():

        raise HttpError(
            400,
            "Anda sudah memberikan review."
        )
    
    review = Review.objects.create(
        student=request.auth,
        course=course,
        rating=data.rating,
        review=data.review
    )

    update_course_average_rating(course)

    log_activity(
        user=request.auth,
        action="CREATE_REVIEW",
        detail={
            "course_id": course.id,
            "course_title": course.title,
            "rating": data.rating,
            "student": request.auth.username
        }
    )

    cache.clear()

    return review

@router.get(
    "/course/{course_id}",
    response=list[ReviewOut]
)
def list_reviews(
    request,
    course_id: int
):

    get_object_or_404(
        Course,
        id=course_id
    )

    return (
        Review.objects
        .filter(course_id=course_id)
        .select_related("student")
        .order_by("-created_at")
    )

@router.patch(
    "/{review_id}",
    auth=JWTAuth(),
    response=ReviewOut
)
def update_review(
    request,
    review_id: int,
    data: ReviewCreate
):

    is_student(request.auth)

    review = get_object_or_404(
        Review,
        id=review_id
    )

    if review.student != request.auth:
        raise HttpError(
            403,
            "Anda bukan pemilik review ini."
        )

    review.rating = data.rating
    review.review = data.review
    review.save(
        update_fields=[
            "rating",
            "review"
        ]
    )

    course = review.course

    update_course_average_rating(course)

    log_activity(
        user=request.auth,
        action="UPDATE_REVIEW",
        detail={
            "course_id": review.course.id,
            "review_id": review.id,
            "rating": review.rating
        }
    )
    cache.clear()

    return review

@router.delete(
    "/{review_id}",
    auth=JWTAuth()
)
def delete_review(
    request,
    review_id: int
):

    is_student(request.auth)

    review = get_object_or_404(
        Review,
        id=review_id
    )

    if review.student != request.auth:
        raise HttpError(
            403,
            "Anda bukan pemilik review ini."
        )

    course = review.course

    review.delete()

    update_course_average_rating(course)

    cache.clear()

    log_activity(
        user=request.auth,
        action="DELETE_REVIEW",
        detail={
            "course_id": course.id,
            "review_id": review_id
        }
    )

    return {
        "message": "Review berhasil dihapus."
    }