from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CourseQuerySet(models.QuerySet):
    def for_listing(self):
        return self.select_related('instructor', 'category')\
                   .prefetch_related('lessons')
    
class EnrollmentQuerySet(models.QuerySet):
    def for_student_dashboard(self):
        return self.select_related('course')\
                   .prefetch_related('progress_set__lesson')

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default='student'
    )

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children'
        )
    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'instructor'}
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    objects = CourseQuerySet.as_manager()
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title
    

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    objects = EnrollmentQuerySet.as_manager()
    enrolled_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('student', 'course')
    def __str__(self):
        return f"{self.student} - {self.course}"
    

class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.enrollment.student.username} - {self.lesson.title} ({status})"

#


