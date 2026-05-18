from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from app.extensions import db
from app.models import Users  

class Userschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        sqla_session = db.session
       
       
    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    email = auto_field(required=True, validate=validate.Email())
    password = fields.Str(required=True, load_only=True)
