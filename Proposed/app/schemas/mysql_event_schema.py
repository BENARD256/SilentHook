from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.extensions import db
from app.models import Mysql_events
from marshmallow import validate


class Mysql_eventschema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mysql_events
        load_instance = True
        sqla_session = db.session