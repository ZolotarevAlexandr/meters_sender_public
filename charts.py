from data.counters_record import CountersRecord
import matplotlib
import matplotlib.pyplot as plt
from data import db_session
import logging
matplotlib.use('Agg')


def create_chart(column, user_id):
    db_sess = db_session.create_session()
    logging.debug(f'[charts.py, update_all_charts] Connected to DB')
    values = db_sess.query(column).filter(CountersRecord.user_id == user_id).all()
    differences = []
    for index, val in enumerate(values[1:], start=1):
        differences.append(val[0] - values[index - 1][0])
    plt.grid()
    plt.plot(differences)
    plt.savefig(f'static/{column}_{user_id}.png')
    plt.clf()
    logging.debug(f'[charts.py, update_all_charts] New {column} chart successfully created')


def update_all_charts(user_id):
    try:
        create_chart(CountersRecord.kitchen_hot, user_id)
        create_chart(CountersRecord.kitchen_cold, user_id)
        create_chart(CountersRecord.bathroom_hot, user_id)
        create_chart(CountersRecord.bathroom_cold, user_id)
        create_chart(CountersRecord.electricity, user_id)
        logging.info('[charts.py, update_all_charts] All charts are successfully updated')
    except Exception as e:
        logging.error(f'[charts.py, update_all_charts] '
                      f'While updating charts an error occurred: {e}', exc_info=True)
