from data import db_session
from data.users_model import User

db_session.global_init('db/counters_history.db')
db_sess = db_session.create_session()

user = db_sess.query(User).first()
print(user.user_info[0].receiver_email)
# print(user.counters_records)
