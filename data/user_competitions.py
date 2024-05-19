from .db_session import SqlAlchemyBase
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class User_competitions(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user_competitions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.INT, sqlalchemy.ForeignKey("users.id"))
    type = sqlalchemy.Column(sqlalchemy.INT, sqlalchemy.ForeignKey("competition.id"))
    user = orm.relationship('User')
