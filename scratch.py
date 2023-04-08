import datetime
from data.counters_record import CountersRecord
from data import db_session
import matplotlib.pyplot as plt

db_session.global_init('db/counters_history.db')


def find_record(column, user_id):
    db_session.global_init('db/counters_history.db')
    db_sess = db_session.create_session()
    return db_sess.query(column).filter(CountersRecord.user_id == user_id).first()


def create_chart(column, user_id):
    db_sess = db_session.create_session()
    values = db_sess.query(column).filter(CountersRecord.user_id == user_id).all()
    differences = []
    for index, val in enumerate(values[1:], start=1):
        differences.append(val[0] - values[index - 1][0])
    plt.grid()
    plt.plot(differences)
    plt.savefig(f'static/{column}.png')
    plt.clf()


create_chart(CountersRecord.kitchen_hot, 1)
