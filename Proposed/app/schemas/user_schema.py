from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate
from app.extensions import db
from app.models import Users

class Userschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        sqla_session = db.session

    ## Exclude password hash from serialization for security reasons
        password_hash = auto_field(load_only=True)
        exclude("password_hash")
    
    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    email = auto_field(required=True, validate=validate.Email())
    password = fields.Str(required=True, load_only=True)