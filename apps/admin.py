from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Course, Lesson, Enrollment, Progress
# Register your models here.
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category')
    list_select_related = ('instructor', 'category')
    search_fields = ('title',)
    list_filter = ('category',)
    inlines = [LessonInline]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

    # add_fieldsets = BaseUserAdmin.add_fieldsets + (
    #     ('Role Info', {'fields': ('role',)}),
    # )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_select_related = ('parent',)
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_select_related = ('course',)
    search_fields = ('title',)
    list_filter = ('course',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_select_related = ('student', 'course')
    search_fields = ('student__username', 'course__title')
    list_filter = ('course',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(role='student')

        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed')
    list_select_related = ('enrollment', 'lesson')
    search_fields = ('enrollment__student__username', 'enrollment__course__title', 'lesson__title')
    list_filter = ('completed',)

