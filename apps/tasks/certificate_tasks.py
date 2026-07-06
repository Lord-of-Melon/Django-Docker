from celery import shared_task


@shared_task
def generate_certificate(student_name, course_title):

    print("=" * 60)

    print("CERTIFICATE TASK")

    print(f"Student : {student_name}")

    print(f"Course  : {course_title}")

    print("Certificate generated successfully.")

    print("=" * 60)

    return True