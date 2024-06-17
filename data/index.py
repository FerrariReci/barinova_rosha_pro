from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Index(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'index'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.Date, index=True, nullable=True)