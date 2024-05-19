from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Competition(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'competition'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.TEXT, index=True, unique=True, nullable=True)
