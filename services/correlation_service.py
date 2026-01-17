from datetime import datetime, timedelta, timezone
from models.event_log import EventLog
from models.alert import Alert
from extensions import db
import json

def detect_correlated_attack(user_id):
    """
    Detects multi-layer attacks by correlating
    login and behavior alerts within 10 minutes.
    """

    ten_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=10)

    recent_alerts = EventLog.query.filter(
        EventLog.user_id == user_id,
        EventLog.event_type == "SECURITY_ALERT",
        EventLog.created_at >= ten_minutes_ago
    ).count()

    if recent_alerts >= 2:
        alert = Alert(
            user_id=user_id,
            severity="HIGH",
            message="Correlated multi-layer attack detected"
        )
        db.session.add(alert)
        db.session.commit()

        return True

    return False

    # Correlation engine checks:
    # Same user ID
    # Same time window (last 10 minutes)
    # More than one security alert