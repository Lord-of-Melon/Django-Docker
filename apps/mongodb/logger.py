from datetime import datetime
from .client import db


def log_activity(user, action, detail=None):
    """
    Menyimpan activity log ke MongoDB
    """

    db.activity_logs.insert_one({
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "action": action,
        "detail": detail or {},
        "timestamp": datetime.utcnow()
    })