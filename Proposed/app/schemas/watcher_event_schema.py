from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import Baits
from marshmallow import validate
from app.extensions import db
from app.models import Watcher_events

IP_REGEX = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

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