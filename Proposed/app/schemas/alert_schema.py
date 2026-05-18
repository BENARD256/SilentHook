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

class Watcher_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Watcher_events
        load_instance = True
        sqla_session = db.session

    token = auto_field(required=True)
    user = auto_field(required=True)
    path = auto_field(required=True)
    access = auto_field(required=True)
    process = auto_field(required=True)
    source_ip = auto_field(required=True, validate=validate.Regexp(IP_REGEX, error="Invalid IP"))
    event_time = auto_field(required=True)

class Mysql_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mysql_events
        load_instance = True
        sqla_session = db.session