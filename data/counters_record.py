import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class CountersRecord(SqlAlchemyBase):
    __tablename__ = 'counters record'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, unique=True)
    kitchen_hot = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    kitchen_cold = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    bathroom_hot = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    bathroom_cold = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    electricity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False, default=datetime.date.today())

    def __repr__(self):
        return f'''
Кухня, горячая вода: {self.kitchen_hot}
Кухня, холодная вода: {self.kitchen_cold}
Ванная, горячая вода: {self.bathroom_hot}
Ванная, холодная вода: {self.bathroom_cold}
Электричество: {self.electricity}
Дата: {self.date.strftime('%d.%m.%Y')}
        '''

    def __str__(self):
        return f'''
Кухня, горячая вода: {self.kitchen_hot}
Кухня, холодная вода: {self.kitchen_cold}
Ванная, горячая вода: {self.bathroom_hot}
Ванная, холодная вода: {self.bathroom_cold}
Электричество: {self.electricity}
Дата: {self.date.strftime('%d.%m.%Y')}
        '''
