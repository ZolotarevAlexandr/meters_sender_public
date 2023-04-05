import matplotlib
import matplotlib.pyplot as plt
from data import db_session
import logging
matplotlib.use('Agg')


def create_chart(column):
    db_sess = db_session.create_session()
    logging.debug(f'[charts.py, update_all_charts] Connected to DB')
    values = db_sess.query(column).all()
    differences = []
    for index, val in enumerate(values[1:], start=1):
        differences.append(val[0] - values[index - 1][0])
    plt.grid()
    plt.plot(differences)
    plt.savefig(f'static/{column}.png')
    plt.clf()
    logging.debug(f'[charts.py, update_all_charts] New {column} chart successfully created')


def update_all_charts():
    from data.counters_record import CountersRecord
    try:
        create_chart(CountersRecord.kitchen_hot)
        create_chart(CountersRecord.kitchen_cold)
        create_chart(CountersRecord.bathroom_hot)
        create_chart(CountersRecord.bathroom_cold)
        create_chart(CountersRecord.electricity)
        logging.info('[charts.py, update_all_charts] All charts are successfully updated')
    except Exception as e:
        logging.error(f'[charts.py, update_all_charts] '
                      f'While updating charts an error occurred: {e}', exc_info=True)
