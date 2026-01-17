from datetime import datetime, timezone
from extensions import db

class RiskScore(db.Model):
    __tablename__ = "risk_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)
    last_updated = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
