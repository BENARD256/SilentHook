from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate
from app.extensions import db
from app.models import Alert_history


class AlertHistorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alert_history
        load_instance = True
        sqla_session = db.session

    # System-managed fields are output-only to prevent user spoofing
    id = auto_field(dump_only=True)
    token = auto_field(dump_only=True)
    recipient_addr = auto_field(required=True, validate=validate.Email())
    
    delivery_status = auto_field(required = False)  # This field will be updated by the system, not the user