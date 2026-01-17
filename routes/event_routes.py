from flask import Blueprint, request, jsonify
from models.event_log import EventLog
from extensions import db
import json

#behavior detection
from services.behavior_anomaly_service import is_behavior_anomalous
from services.risk_scoring_service import update_risk_score
from services.alert_service import evaluate_and_create_alert


# Create Blueprint
event_bp = Blueprint("event_bp", __name__)

@event_bp.route("/log-event", methods=["POST"])
def log_event():
    """
    Logs a security-related event into the database.
    Expected JSON input:
    {
        "user_id": 1,
        "event_type": "LOGIN_ATTEMPT",
        "ip": "192.168.1.10"
    }
    """

    data = request.get_json()

    # Basic validation
    if not data or "user_id" not in data or "event_type" not in data:
        return jsonify({
            "error": "Invalid input data"
        }), 400

    try:
        event = EventLog(
            user_id=data["user_id"],
            event_type=data["event_type"],
            event_data=json.dumps(data)  # store full event payload
        )

        db.session.add(event)
        db.session.commit()

        return jsonify({
            "message": "Event logged successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to log event",
            "details": str(e)
        }), 500


@event_bp.route("/log-action", methods=["POST"])
def log_user_action():
    """
    Logs general user activity for behavior analysis.
    Expected JSON:
    {
        "user_id": 1,
        "action_type": "PAGE_ACCESS",
        "resource": "/reports"
    }
    """

    data = request.get_json()

    if not data or "user_id" not in data or "action_type" not in data:
        return jsonify({"error": "Invalid action data"}), 400

    event = EventLog(
        user_id=data["user_id"],
        event_type=data["action_type"],
        event_data=json.dumps(data)
    )

    db.session.add(event)
    db.session.commit()

    # 🔴 Check for abnormal behavior
    if is_behavior_anomalous(data["user_id"]):
        update_risk_score(data["user_id"], 20)
        evaluate_and_create_alert(data["user_id"])


    return jsonify({"message": "User action logged"}), 201
