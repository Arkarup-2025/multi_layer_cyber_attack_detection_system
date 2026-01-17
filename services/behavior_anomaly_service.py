from datetime import datetime, timedelta, timezone
from models.event_log import EventLog

def is_behavior_anomalous(user_id):
    """
    Returns True if user performs more than
    10 actions in the last 1 minute.
    """

    one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

    action_count = EventLog.query.filter(
        EventLog.user_id == user_id,
        EventLog.created_at >= one_minute_ago,
        EventLog.event_type.notin_([
            "SUCCESSFUL_LOGIN",
            "FAILED_LOGIN",
            "SECURITY_ALERT"
        ])
    ).count()

    return action_count > 10
