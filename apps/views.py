from django.shortcuts import render
from apps.models import Course

def course_list(request):
    courses = Course.objects.for_listing()
    return render(request, "courses/list.html", {"courses": courses})