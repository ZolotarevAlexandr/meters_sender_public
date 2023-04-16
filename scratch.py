from data.counters_record import CountersRecord
from data import db_session
from data.users_model import User

db_session.global_init('db/counters_history.db')
db_sess = db_session.create_session()

user = db_sess.query(User).all()[0]

COLUMNS = [CountersRecord.kitchen_hot, CountersRecord.kitchen_cold, CountersRecord.bathroom_hot,
           CountersRecord.bathroom_cold, CountersRecord.electricity]

lists = {}

for column in COLUMNS:
    values = [getattr(record, column.key) for record in user.counters_records]
    lists[column.key] = values

print(lists)
