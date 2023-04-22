from flask_restful import Resource
from flask import jsonify
from data.counters_record import CountersRecord
from flask_login import current_user
from data import db_session
import datetime


class MetersResource(Resource):
    def get(self, date):
        user_id = current_user.get_id()
        if not user_id:
            return jsonify({'error': 'login required'})
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        db_sess = db_session.create_session()
        record = db_sess.query(CountersRecord).filter(CountersRecord.user_id == user_id,
                                                      CountersRecord.date == date).first()
        if not record:
            return jsonify({'error': 'Not found'})
        return jsonify({
            'record':
                record.to_dict(only=('kitchen_hot', 'kitchen_cold', 'bathroom_hot',
                                     'bathroom_cold', 'electricity', 'date'))
        })


class MetersListResource(Resource):
    def get(self):
        user_id = current_user.get_id()
        if not user_id:
            return jsonify({'error': 'login required'})
        db_sess = db_session.create_session()
        records = db_sess.query(CountersRecord).filter(CountersRecord.user_id == user_id).all()
        return jsonify({
            'records':
                [record.to_dict(only=('kitchen_hot', 'kitchen_cold', 'bathroom_hot',
                                      'bathroom_cold', 'electricity', 'date')) for record in records]
        })
