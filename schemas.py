from models import db, Users, Baits, Triggers, Alerts, Watcher_events, Mysql_events

from marshmallow import validate, ValidationError

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

import re # IP Validation Lib

class Userschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        sqla_session = db.session # SQLAlchemy session for database operations

    username = auto_field(required=True)
    email = auto_field(required=True, validate=validate.Email())
    password = auto_field(required=True,load_only=True) # Be sure Its not loaded in API responses  #, validate=validate.Length(min=8))
    

class Baitsschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Baits
        load_instance = True # True returns database models instead of dictionary
    name = auto_field(required=True)
    abbrev = auto_field(required=True)
    type = auto_field(required=True)
    description = auto_field(required=True)
    bait_path = auto_field(required=True, load_only=True) # Not loaded in API responses



class Triggerschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Triggers
        load_instance = True #False # If True, deserialization returns database model instances instead of dictionary
        sqla_session = db.session # SQLAlchemy session for database operations
    id = auto_field(required=True)
    token = auto_field(required=True)
    reminder = auto_field(required=True)
    callback_email = auto_field(required=False, validate=validate.Email())
    user_id = auto_field(required=False)
    bait_id = auto_field(required=False)
    created_at = auto_field(dump_only=True) # Not required in input, only in output


class Alertschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alerts
        load_instance = True # Request bring in Json Data
        sqla_session = db.session

    token = auto_field(required=True)
    source_ip = auto_field(required=True, validate=validate.Regexp(
        r"^(\d{1,3}\.){3}\d{1,3}$",
        error="Invalid IP address format"
    ))
    user_agent = auto_field(required=True)

    event_time = auto_field(required=True)
 

class Watcher_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Watcher_events
        load_instance = True # json loads db object
        sqla_session = db.session

    token = auto_field(required=True)
    user = auto_field(required=True)
    path = auto_field(required=True)
    access = auto_field(required=True)
    process = auto_field(required=True)
    source_ip = auto_field(required=True,validate=validate.Regexp(
        r"^(\d{1,3}\.){3}\d{1,3}$",
        error="Invalid IP address format"
    ))
    event_time = auto_field(required=True)


class Mysql_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mysql_events
        load_instance = True