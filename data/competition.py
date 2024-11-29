from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Competition(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'competition'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.TEXT, index=True, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, index=True, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.TEXT, index=True, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    place = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    res = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    categories = sqlalchemy.Column(sqlalchemy.VARCHAR, index=True, nullable=True)
    distances = sqlalchemy.Column(sqlalchemy.VARCHAR, index=True, nullable=True)
    user_competitions = orm.relationship("User_competitions", back_populates='competition')