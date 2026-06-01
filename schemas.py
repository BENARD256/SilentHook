from models import db, Users, Baits, Triggers, Alerts, Watcher_events, Alert_history

from marshmallow import validate, validates, ValidationError

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
import bleach, unicodedata
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
    image_path = auto_field(required=True)



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

    @validates('reminder')
    def validate_reminder(self, value):
        try:
            # Normalizing unicode characters
            value = unicodedata.normalize('NFKC', value)
            
            # Stripping all HTML tags entirely using bleach
            cleaned = bleach.clean(value, tags=[], attributes={}, strip=True)
            
            if cleaned != value: # Verifying tags are stripped incase present.
                raise ValidationError("Reminder contains invalid characters.")
            
            # Stripping JS injection patterns not caught by tag stripping
            if re.search(r'javascript:|vbscript:|data:|on\w+\s*=|expression\s*\(', cleaned, re.IGNORECASE):
                raise ValidationError("Reminder contains invalid characters.")
            
            if '\x00' in value: # Block null bytes
                raise ValidationError("Reminder contains invalid characters.")

            if len(cleaned.strip()) < 3: # Length Validation
                raise ValidationError("Reminder must be at least 3 characters.")
            if len(cleaned) > 250:
                raise ValidationError("Reminder must not exceed 250 characters.")
            
            return cleaned.strip()

        except ValidationError:
            raise # raise Validation error

        except Exception as e:
            print("VALIDATOR CRASH:", type(e).__name__, e)
            raise ValidationError("Reminder validation failed unexpectedly.")

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


class Alert_historySchema(SQLAlchemyAutoSchema):  
    class Meta:
        model = Alert_history
        load_instance = False # When Deserializing (Loading) Return Database Objects
        sqla_session = db.session
    
    id = auto_field(required=True, load_only=True) # Not Displayed in Api Responses
    token = auto_field(required=True)
    bait_type = auto_field(required=True)
    source_ip = auto_field(required=True)
    event_time = auto_field(required=True, dump_only=True) # Not required in input, only displayed in  API output
    user_id = auto_field(required=True, load_only=True) # Not displayed in API response
