from datetime import datetime
from .client import db


def log_activity(user, action, detail=None):

    document = {
        "user_id": user.id if user else None,
        "username": user.username if user else "Anonymous",
        "action": action,
        "detail": detail or {},
        "created_at": datetime.utcnow(),
    }

    db.activity_logs.insert_one(document)