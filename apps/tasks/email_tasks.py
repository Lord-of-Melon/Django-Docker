from celery import shared_task

@shared_task
def send_enrollment_email(student_name, course_title):

    print("=" * 60)

    print("EMAIL TASK")

    print(f"Student : {student_name}")

    print(f"Course  : {course_title}")

    print("Enrollment email berhasil dikirim.")

    print("=" * 60)

    return True