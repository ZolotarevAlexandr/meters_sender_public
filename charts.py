from data.counters_record import CountersRecord
import matplotlib
import matplotlib.pyplot as plt
import logging

matplotlib.use('Agg')

COLUMNS = [CountersRecord.kitchen_hot, CountersRecord.kitchen_cold, CountersRecord.bathroom_hot,
           CountersRecord.bathroom_cold, CountersRecord.electricity]


def update_all_charts(user):
    try:
        lists = {}

        for column in COLUMNS:
            values = [getattr(record, column.key) for record in user.counters_records]
            lists[column.key] = values

        for key, values in lists.items():
            create_chart(key, values, user.get_id())

        logging.debug(f'[charts.py, update_all_charts] All charts for user {user.login} updated')
    except Exception as e:
        logging.error(f'[charts.py, update_all_charts] A following error occurred: {e}',
                      exc_info=True)


def create_chart(column, values, user_id):
    differences = []
    for index, val in enumerate(values[1:], start=1):
        differences.append(val - values[index - 1])

    plt.grid()
    plt.plot(differences)
    plt.savefig(f'static/{column}_{user_id}.png')
    plt.clf()
