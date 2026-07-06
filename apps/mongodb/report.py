from apps.mongodb.client import db


def course_completion_report():
    """
    Report completion setiap course.
    """

    pipeline = [
        {
            "$group": {
                "_id": "$course_title",
                "students": {
                    "$sum": 1
                },
                "avg_completion": {
                    "$avg": "$completion_rate"
                },
                "max_completion": {
                    "$max": "$completion_rate"
                },
                "min_completion": {
                    "$min": "$completion_rate"
                }
            }
        },
        {
            "$sort": {
                "avg_completion": -1
            }
        }
    ]

    return list(
        db.learning_analytics.aggregate(pipeline)
    )

def most_popular_courses():

    pipeline = [
        {
            "$group": {
                "_id": "$course_title",
                "enrollments": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "enrollments": -1
            }
        }
    ]

    return list(
        db.learning_analytics.aggregate(pipeline)
    )
def student_progress_report():

    pipeline = [
        {
            "$project": {
                "_id": 0,
                "student": "$student_username",
                "course": "$course_title",
                "completion": "$completion_rate"
            }
        },
        {
            "$sort": {
                "completion": -1
            }
        }
    ]

    return list(
        db.learning_analytics.aggregate(pipeline)
    )