from handyhub_project.api.models.tradesman import Tradesman
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class TradesmanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tradesman
        load_instance = True
