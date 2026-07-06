import csv
import os

from celery import shared_task
from django.conf import settings

from apps.models import Course


@shared_task
def export_course_report():

    report_dir = os.path.join(
        settings.BASE_DIR,
        "reports"
    )

    os.makedirs(
        report_dir,
        exist_ok=True
    )

    filename = os.path.join(
        report_dir,
        "course_report.csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "ID",
            "Title",
            "Instructor",
            "Category"
        ])

        for course in Course.objects.select_related(
            "instructor",
            "category"
        ):

            writer.writerow([
                course.id,
                course.title,
                course.instructor.username,
                course.category.name if course.category else "-"
            ])

    print("=" * 60)
    print("REPORT GENERATED")
    print(filename)
    print("=" * 60)

    return filename