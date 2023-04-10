import sqlalchemy

from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from encryption_module import encrypt_password, decrypt_password


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_user_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    receiver_email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_mail_app_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    counters_records = orm.relationship("CountersRecord", back_populates="user")

    def set_user_password(self, password):
        self.hashed_user_password = encrypt_password(password)

    def check_user_password(self, password):
        return decrypt_password(self.hashed_user_password) == password

    def set_mail_app_password(self, password):
        self.hashed_mail_app_password = encrypt_password(password)

    def get_id(self):
        return self.id
