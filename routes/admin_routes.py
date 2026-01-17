from flask import Blueprint, jsonify
from models.alert import Alert
from models.risk_score import RiskScore
from models.event_log import EventLog
from models.user import User

import json

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    result = []

    for alert in alerts:
        risk = RiskScore.query.filter_by(user_id=alert.user_id).first()

        result.append({
            "id": alert.id,
            "user_id": alert.user_id,
            "severity": alert.severity,
            "message": alert.message,
            "risk_score": risk.score if risk else 0,
            "created_at": alert.created_at.isoformat()
        })


    return jsonify(result), 200


@admin_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        for user in users
    ])

@admin_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    risk = RiskScore.query.filter_by(user_id=user_id).first()
    
    # recent alerts
    alerts = Alert.query.filter_by(user_id=user_id)\
        .order_by(Alert.created_at.desc()).limit(5).all()
    
    # 10 activity logs 
    events = EventLog.query.filter_by(user_id=user_id)\
        .order_by(EventLog.created_at.desc()).limit(10).all()

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "risk_score": risk.score if risk else 0,
        "recent_alerts": [
            {
                "severity": a.severity,
                "message": a.message,
                "created_at": a.created_at.isoformat()
            } for a in alerts
        ],
        "recent_events": [
            {
                "event_type": e.event_type,
                "resource": json.loads(e.event_data).get("resource", "N/A")
                            if e.event_data else "N/A",
                "created_at": e.created_at.isoformat()
            } for e in events
        ]

    })

@admin_bp.route("/user/<int:user_id>/timeline", methods=["GET"])
def user_timeline(user_id):
    events = EventLog.query.filter_by(user_id=user_id)\
        .order_by(EventLog.created_at.asc()).all()

    timeline = []
    for e in events:
        timeline.append({
            "event_type": e.event_type,
            "created_at": e.created_at.isoformat()
        })

    return jsonify(timeline)
