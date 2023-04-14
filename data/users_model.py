import sqlalchemy

from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from encryption_module import encrypt_info, decrypt_info


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_user_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    counters_records = orm.relationship("CountersRecord", back_populates="user")
    user_info = orm.relationship("UserInfo", back_populates="user")

    def set_user_password(self, password):
        self.hashed_user_password = encrypt_info(password)

    def check_user_password(self, password):
        return decrypt_info(self.hashed_user_password) == password

    def get_id(self):
        return self.id
