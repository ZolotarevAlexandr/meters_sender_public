import sqlalchemy
from cryptography.fernet import Fernet

from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase

KEY = b'wJUj3MW9-s3m-nSEpKG8pHFY_Z0NttYXFlRK9QIZkZ8='


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_user_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    receiver_email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_mail_app_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    counters_records = orm.relationship("CountersRecord", back_populates="user")

    def set_user_password(self, password):
        self.hashed_user_password = Fernet(KEY).encrypt(str.encode(password))

    def check_user_password(self, password):
        return Fernet(KEY).decrypt(self.hashed_user_password).decode() == password

    def set_mail_app_password(self, password):
        self.hashed_mail_app_password = Fernet(KEY).encrypt(str.encode(password))

    def get_id(self):
        return self.id
