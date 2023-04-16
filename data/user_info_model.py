import sqlalchemy

from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from encryption_module import encrypt_info, decrypt_info


class UserInfo(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user info'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, unique=True)

    receiver_email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_mail_app_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email_server = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    additional_info = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name_surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    personal_account = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    kitchen_hot_serial = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    kitchen_cold_serial = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    bathroom_hot_serial = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    bathroom_cold_serial = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    electricity_serial = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), unique=True)
    user = orm.relationship("User", back_populates="user_info")

    def set_mail_app_password(self, password):
        self.hashed_mail_app_password = encrypt_info(password)

    def check_mail_app_password(self, password):
        return decrypt_info(self.hashed_mail_app_password) == password

    def set_additional_info(self, info):
        self.additional_info = encrypt_info(info)

    def set_name(self, name):
        self.name_surname = encrypt_info(name)

    def set_phone(self, phone):
        self.phone = encrypt_info(phone)

    def set_personal_account(self, account):
        self.personal_account = encrypt_info(account)
