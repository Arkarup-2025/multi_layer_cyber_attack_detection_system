from models.alert import Alert
from models.risk_score import RiskScore
from extensions import db
from datetime import datetime, timedelta, timezone

from services.correlation_service import detect_correlated_attack


def evaluate_and_create_alert(user_id):
    risk = RiskScore.query.filter_by(user_id=user_id).first()

    if not risk:
        return

    if risk.score <= 20:
        severity = "LOW"
    elif risk.score <= 50:
        severity = "MEDIUM"
    else:
        severity = "HIGH"

    # 🔴 Avoid duplicate alerts within 10 minutes
    ten_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=10)
    recent_alert = Alert.query.filter(
        Alert.user_id == user_id,
        Alert.severity == severity,
        Alert.created_at >= ten_minutes_ago
    ).first()

    if recent_alert:
        return

    alert = Alert(
        user_id=user_id,
        severity=severity,
        message="User risk score crossed threshold"
    )

    db.session.add(alert)
    db.session.commit()

    detect_correlated_attack(user_id)

