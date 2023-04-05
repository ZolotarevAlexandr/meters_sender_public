from flask import Flask
from data import db_session
import auth_pages
import main_app
import logging

logging.basicConfig(
    filename='logs.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.INFO
)

app = Flask(__name__)
app.config['SECRET_KEY'] = '22051977'
app.config['DEBUG'] = True


def main():
    logging.info('[main.py, main] App started')
    db_session.global_init('db/counters_history.db')
    logging.info('[main.py, main] DB global initialization complete')
    app.register_blueprint(auth_pages.blueprint)
    app.register_blueprint(main_app.blueprint)
    app.run(port=5000, host='192.168.1.182')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.fatal(f'[main.py, main] Fatal error: {e}', exc_info=True)
