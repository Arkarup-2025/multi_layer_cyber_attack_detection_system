from datetime import datetime, timezone
from models.risk_score import RiskScore
from extensions import db

def update_risk_score(user_id, points):
    risk = RiskScore.query.filter_by(user_id=user_id).first()

    if not risk:
        risk = RiskScore(user_id=user_id, score=0)

    risk.score += points
    risk.last_updated = datetime.now(timezone.utc)

    db.session.add(risk)
    db.session.commit()
