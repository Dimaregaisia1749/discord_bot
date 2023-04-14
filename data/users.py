import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    avatar_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    max_hp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    crit_chance = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    crit_damage = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    armor = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    base_damage = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rank = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coins = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tesseracts = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    expirience = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    items = orm.relationship("Item", back_populates="user")
