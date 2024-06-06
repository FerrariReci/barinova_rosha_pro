from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Competition(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'competition'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.TEXT, index=True, unique=True, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer, index=True, unique=True, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, index=True, unique=True, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.TEXT, index=True, unique=True, nullable=True)
    user_competitions = orm.relationship("User_competitions", back_populates='competition')