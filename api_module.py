from flask_restful import Resource
from flask import jsonify
from data.counters_record import CountersRecord
from flask_login import current_user
from data import db_session
import datetime
import logging


class MetersResource(Resource):
    def get(self, date):
        try:
            user_id = current_user.get_id()
            if not user_id:
                logging.info('[api_module.py, get] Unauthorized api request')
                return jsonify({'error': 'login required'})
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            db_sess = db_session.create_session()
            record = db_sess.query(CountersRecord).filter(CountersRecord.user_id == user_id,
                                                          CountersRecord.date == date).first()
            if not record:
                logging.debug(f'[api_module.py, get] record for date {date} for user {user_id} not found')
                return jsonify({'error': 'Not found'})
            logging.info(f'[api_module.py, get] Successful api request for date {date} by user {user_id}')
            return jsonify({
                'record':
                    record.to_dict(only=('kitchen_hot', 'kitchen_cold', 'bathroom_hot',
                                         'bathroom_cold', 'electricity', 'date'))
            })
        except Exception as e:
            logging.error(f'[api_module.py, get] error {e} occurred')
            return jsonify({'error': 'unknown error'})


class MetersListResource(Resource):
    def get(self):
        try:
            user_id = current_user.get_id()
            if not user_id:
                logging.info('[api_module.py, get] Unauthorized api request')
                return jsonify({'error': 'login required'})
            db_sess = db_session.create_session()
            records = db_sess.query(CountersRecord).filter(CountersRecord.user_id == user_id).all()
            logging.info(f'[api_module.py, get] Successful api request by user {user_id}')
            return jsonify({
                'records':
                    [record.to_dict(only=('kitchen_hot', 'kitchen_cold', 'bathroom_hot',
                                          'bathroom_cold', 'electricity', 'date')) for record in records]
            })
        except Exception as e:
            logging.error(f'[api_module.py, get] error {e} occurred')
            return jsonify({'error': 'unknown error'})
