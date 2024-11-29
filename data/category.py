from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Category(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'category'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    gender = sqlalchemy.Column(sqlalchemy.VARCHAR, index=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.TEXT, index=True, nullable=True)