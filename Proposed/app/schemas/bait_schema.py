from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import Baits

class Baitsschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Baits
        load_instance = True

    name = auto_field(required=True)
    abbrev = auto_field(required=True)
    type = auto_field(required=True)
    description = auto_field(required=True)
    bait_path = auto_field(required=True, load_only=True)
    image_path = auto_field(required=True)