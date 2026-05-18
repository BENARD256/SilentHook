from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate
from app.extensions import db
from app.models import Alerts, Watcher_events, Mysql_events

IP_REGEX = r"^(\d{1,3}\.){3}\d{1,3}$"

class Alertschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alerts
        load_instance = True
        sqla_session = db.session

    token = auto_field(required=True)
    source_ip = auto_field(required=True, validate=validate.Regexp(IP_REGEX, error="Invalid IP"))
    user_agent = auto_field(required=True)
    event_time = auto_field(required=True)

