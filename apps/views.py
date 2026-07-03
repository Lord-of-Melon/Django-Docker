from django.shortcuts import render
from apps.models import Course, Enrollment

def course_list(request):
    courses = Course.objects.for_listing()
    return render(request, "courses/list.html", {"courses": courses})

def dashboard(request):
    enrollments = (
        Enrollment.objects
        .for_student_dashboard()
        .filter(student=request.user)
    )

    return render(request, "dashboard.html", {
        "enrollments": enrollments
    })