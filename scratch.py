import datetime
from data.counters_record import CountersRecord
from data import db_session


def find_today_record():
    db_session.global_init('db/counters_history.db')
    db_sess = db_session.create_session()
    return db_sess.query(CountersRecord).filter(CountersRecord.date == datetime.date.today()).first()


a = find_today_record()
print(type(a.id))
print(type(a.kitchen_hot))
print((a.date.strftime('%d.%m.%Y')))
print(a)
