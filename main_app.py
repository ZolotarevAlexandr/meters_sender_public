import flask
from flask import render_template, redirect
from flask_login import login_required, current_user

from data.counters_form import CountersForm
from data.counters_record import CountersRecord
from data import db_session

from charts import update_all_charts
import email_module

import logging


blueprint = flask.Blueprint(
    'main_app',
    __name__,
    template_folder='templates'
)


@blueprint.route('/')
def main_page():
    return render_template('main_page.html')


@blueprint.route('/send', methods=['GET', 'POST'])
@login_required
def form_page():
    try:
        form = CountersForm()
        if form.validate_on_submit():
            logging.debug('[main_app.py, form_page] Form received')
            db_sess = db_session.create_session()
            logging.debug('[main_app.py, form_page] Connected to DB')
            counters = CountersRecord()

            counters.kitchen_hot = form.kitchen_hot.data
            counters.kitchen_cold = form.kitchen_cold.data
            counters.bathroom_hot = form.bathroom_hot.data
            counters.bathroom_cold = form.bathroom_cold.data
            counters.electricity = form.electricity.data
            counters.user_id = current_user.get_id()

            db_sess.add(counters)
            db_sess.commit()

            logging.info('[main_app.py, form_page] New record added to database')

            email_module.send_counters_info(counters, current_user)
            return redirect('/success')
        return render_template('form.html', title='Counters', form=form)
    except Exception as e:
        logging.error(f'[main_app.py, form_page] A following error occurred: {e}', exc_info=True)
        redirect(f'/error/{e}')


@blueprint.route('/success')
def success():
    return render_template('success.html')


@blueprint.route('/error/<error_name>')
def show_error(error_name):
    return render_template('error.html', error_name=error_name)


@blueprint.route('/help')
def show_instruction():
    return render_template('help.html')


@blueprint.route('/history')
@login_required
def history():
    try:
        update_all_charts(current_user.get_id())
        db_sess = db_session.create_session()
        logging.debug('[main_app.py, history] Connected to DB')
        all_records = db_sess.query(CountersRecord).filter(CountersRecord.user_id == current_user.get_id()).all()[::-1]
        logging.debug('[main_app.py, form_page] History successfully loaded')
        return render_template('history.html', history=all_records, user_id=current_user.get_id())
    except Exception as e:
        logging.error(f'[main_app.py, history] A following error occurred: {e}', exc_info=True)
        redirect(f'/error/{e}')
