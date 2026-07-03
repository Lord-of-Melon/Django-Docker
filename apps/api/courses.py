from ninja import Router
from apps.models import Course, Category
from .schemas import CourseOut, CourseCreate
from django.shortcuts import get_object_or_404
from .security import JWTAuth
from .permissions import is_admin, is_course_owner, is_instructor

router = Router(tags=["Courses"])


@router.get("/", response=list[CourseOut])
def list_courses(request):
    return Course.objects.for_listing()

@router.get("/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return get_object_or_404(
        Course.objects.for_listing(),
        id=course_id
    )

@router.post("/", auth=JWTAuth(), response=CourseOut)
def create_course(request, data: CourseCreate):

    is_instructor(request.auth)

    category = Category.objects.get(id=data.category_id)

    course = Course.objects.create(
        title=data.title,
        instructor=request.auth,
        category=category
    )

    return course

@router.patch("/{course_id}", auth=JWTAuth(), response=CourseOut)
def update_course(request, course_id: int, data: CourseCreate):

    course = get_object_or_404(Course, id=course_id)

    is_course_owner(request.auth, course)

    course.title = data.title
    course.category = Category.objects.get(id=data.category_id)

    course.save()

    return course

@router.delete("/{course_id}", auth=JWTAuth())
def delete_course(request, course_id: int):

    is_admin(request.auth)

    course = get_object_or_404(Course, id=course_id)

    course.delete()

    return {
        "message": "Course berhasil dihapus."
    }