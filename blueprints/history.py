from models import db, Triggers, Alert_history
from schemas import Triggerschema, Alert_historySchema, ValidationError

from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from utils import api_response

from sqlalchemy import func, cast, Date # Aids in Filtering for statistics from history

# Triggers. For Baits That Dint Trigger

history_api_bp = Blueprint('alert_history', __name__, url_prefix="/api/v1/history")

alerthistory_schema = Alert_historySchema()


@history_api_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity() # 6

    # All Deployed
    total_deployed = Triggers.query.filter_by(user_id=user_id).count()

    # All baits Fired
    total_triggered = Alert_history.query.filter_by(user_id=user_id).count()

    not_triggered = total_deployed - total_triggered

    # How Often @ Bait Type is Triggered.
    bait_counts = (
        db.session.query(
            Alert_history.bait_type,
            func.count(Alert_history.id).label('count')
        )
        .filter(Alert_history.user_id == user_id)
        .group_by(Alert_history.bait_type)
        .order_by(func.count(Alert_history.id).desc())
        .all()
    )

    bait_frequency = [
        {'bait_type': row.bait_type, 'count': row.count}
        for row in bait_counts
    ]

    # Triggers Overtime (For a Line Chart). How many alerts per day(date)
    daily_triggers = (
        db.session.query(
            cast(Alert_history.event_time, Date).label('date'),
            func.count(Alert_history.id).label('count')
        )
        .filter(Alert_history.user_id == user_id)
        .group_by(cast(Alert_history.event_time, Date))
        .order_by(cast(Alert_history.event_time, Date))
        .all()
    )

    triggers_over_time = [
        {'date': str(row.date), 'count': row.count}
        for row in daily_triggers
    ]

    # Top Source IPs (For Table) . 5 Most frequent IPs that triggers the baits
    top_ips = (
        db.session.query(
            Alert_history.source_ip,
            func.count(Alert_history.id).label('count')
        )
        .filter(Alert_history.user_id == user_id)
        .group_by(Alert_history.source_ip)
        .order_by(func.count(Alert_history.id).desc())
        .limit(5)
        .all()
    )

    top_source_ips = [
        {'source_ip': row.source_ip, 'count': row.count}
        for row in top_ips
    ]


    # Most Recent Triggers. a single timestamp of the most recent alert.
    last_trigger = (
        Alert_history.query
        .filter_by(user_id=user_id)
        .order_by(Alert_history.event_time.desc())
        .first()
    )

    last_triggered_at = last_trigger.event_time.isoformat() if last_trigger else None
    
    
    return api_response(
        data = {
            'total_deployed': total_deployed,           # Total Baits Deployed
            'total_triggred': total_triggered,          # Count of Baits triggered
            'not_triggered' : not_triggered,            # Count of Bait not triggered Yet
            'bait_frequency': bait_frequency,           # How many times a Bait Type is Triggered.
            'triggers_overtime': triggers_over_time,    # How many alerts per day(date)
            'top_source_ips' : top_source_ips,          # Most frequent IPs that triggers the baits
            'last_activity' : last_triggered_at         # A timestamp of the most recent alert received
        }
    )



@history_api_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    user_id = get_jwt_identity() #6
    
    # All Alerts From history

    all_alerts = Alert_history.query.filter_by(user_id=user_id).all() # DB obj

    return api_response(
        data = {
            'all_alerts' : alerthistory_schema.dump(all_alerts, many=True),
        },
         message = 'Valid'
    )
