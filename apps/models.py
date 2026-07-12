from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

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

    LEVEL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    STATUS_CHOICES = (
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("completed", "Completed"),
    )

    title = models.CharField(max_length=200)

    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "instructor"},
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="beginner",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="inactive",
    )

    student_count = models.PositiveIntegerField(
    default=0
    )

    average_rating = models.FloatField(
        default=0
    )

    objects = CourseQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["level"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title
    

class Enrollment(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )

    # progress = models.PositiveSmallIntegerField(
    #     default=0
    # )
    objects = EnrollmentQuerySet.as_manager()

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} - {self.course}"
    

class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.enrollment.student.username} - {self.lesson.title} ({status})"

class Review(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ]
    )

    review = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("student", "course")

        indexes = [
        models.Index(fields=["course"]),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Wishlist(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("student", "course")

        indexes = [
            models.Index(fields=["student"]),
        ]
        
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

