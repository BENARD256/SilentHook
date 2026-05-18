from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate
from app.extensions import db
from app.models import Triggers

class Triggerschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Triggers
        load_instance = True
        sqla_session = db.session

    token = auto_field(required=True)
    reminder = auto_field(required=True)
    callback_email = auto_field(required=False, validate=validate.Email())
    user_id = auto_field(required=False)
    bait_id = auto_field(required=False)
    created_at = auto_field(dump_only=True)
    