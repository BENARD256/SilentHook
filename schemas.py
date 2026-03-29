from models import db, Users, Baits, Triggers, Alerts, Watcher_events, Mysql_events

from marshmallow import validate, ValidationError

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class Userschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        sqla_session = db.session # SQLAlchemy session for database operations

    username = auto_field(required=True)
    email = auto_field(required=True, validate=validate.Email())
    password = auto_field(required=True) #, validate=validate.Length(min=8))
    

class Baitsschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Baits
        load_instance = True

class Triggerschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Triggers
        load_instance = True


class Alertschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alerts
        load_instance = True

class Watcher_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Watcher_events
        load_instance = True

class Mysql_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mysql_events
        load_instance = True