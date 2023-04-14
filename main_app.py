import flask
from flask import render_template, redirect
from flask_login import login_required, current_user

from data.counters_form import CountersForm
from data.counters_record import CountersRecord
from data.user_info_form import UserInfoForm
from data.user_info_model import UserInfo
from data import db_session

from charts import update_all_charts
import email_module

import logging


blueprint = flask.Blueprint(
    'main_app',
    __name__,
    template_folder='templates'
)


def edit_info(record, form_info):
    record.receiver_email = form_info.receiver_email.data
    record.kitchen_hot_serial = form_info.kitchen_hot_serial.data
    record.kitchen_cold_serial = form_info.kitchen_cold_serial.data
    record.bathroom_hot_serial = form_info.bathroom_hot_serial.data
    record.bathroom_cold_serial = form_info.bathroom_cold_serial.data
    record.electricity_serial = form_info.electricity_serial.data
    record.set_mail_app_password(form_info.app_password.data)
    record.set_additional_info(form_info.additional_info.data)
    record.set_name(form_info.name_surname.data)
    record.set_phone(form_info.phone.data)
    return record


def add_recording(form):
    db_sess = db_session.create_session()
    counters = CountersRecord()

    counters.kitchen_hot = form.kitchen_hot_last.data
    counters.kitchen_cold = form.kitchen_cold_last.data
    counters.bathroom_hot = form.bathroom_hot_last.data
    counters.bathroom_cold = form.bathroom_cold_last.data
    counters.electricity = form.electricity_last.data
    counters.user_id = current_user.get_id()

    db_sess.add(counters)
    db_sess.commit()


@blueprint.route('/')
def main_page():
    return render_template('main_page.html')


@blueprint.route('/send', methods=['GET', 'POST'])
@login_required
def form_page():
    try:
        db_sess = db_session.create_session()
        logging.debug('[main_app.py, form_page] Connected to DB')
        '''
        if not db_sess.query(UserInfo).filter(UserInfo.user_id == current_user.get_id()).first():
            return redirect('/settings')'''

        form = CountersForm()
        if form.validate_on_submit():
            logging.debug('[main_app.py, form_page] Form received')

            prev_record = db_sess.query(CountersRecord).filter(CountersRecord.user_id == current_user.get_id()).all()[-1]
            counters = CountersRecord()

            counters.kitchen_hot = form.kitchen_hot.data
            counters.kitchen_cold = form.kitchen_cold.data
            counters.bathroom_hot = form.bathroom_hot.data
            counters.bathroom_cold = form.bathroom_cold.data
            counters.electricity = form.electricity.data
            counters.user_id = current_user.get_id()

            db_sess.add(counters)
            db_sess.commit()

            if email_module.send_counters_info(counters, prev_record, current_user):
                logging.info('[main_app.py, form_page] New record added to database')
                return redirect('/success')
            return redirect('/error/ошибка при отправке сообщения')
        return render_template('form.html', title='Counters', form=form)
    except Exception as e:
        logging.error(f'[main_app.py, form_page] A following error occurred: {e}', exc_info=True)
        return redirect(f'/error/{e}')


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
        return redirect(f'/error/{e}')


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def edit_info():
    form = UserInfoForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        info_record = db_sess.query(UserInfo).filter(UserInfo.id == current_user.get_id()).first()
        if info_record:
            info_record.receiver_email = form.receiver_email.data
            info_record.kitchen_hot_serial = form.kitchen_hot_serial.data
            info_record.kitchen_cold_serial = form.kitchen_cold_serial.data
            info_record.bathroom_hot_serial = form.bathroom_hot_serial.data
            info_record.bathroom_cold_serial = form.bathroom_cold_serial.data
            info_record.electricity_serial = form.electricity_serial.data
            info_record.set_mail_app_password(form.app_password.data)
            info_record.set_additional_info(form.additional_info.data)
            info_record.set_name(form.name_surname.data)
            info_record.set_phone(form.phone.data)
            info_record.set_personal_account(form.personal_account.data)
            info_record.user_id = current_user.get_id()

            add_recording(form)
            db_sess.commit()
            return redirect('/')

        info_record = UserInfo()
        info_record.receiver_email = form.receiver_email.data
        info_record.kitchen_hot_serial = form.kitchen_hot_serial.data
        info_record.kitchen_cold_serial = form.kitchen_cold_serial.data
        info_record.bathroom_hot_serial = form.bathroom_hot_serial.data
        info_record.bathroom_cold_serial = form.bathroom_cold_serial.data
        info_record.electricity_serial = form.electricity_serial.data
        info_record.set_mail_app_password(form.app_password.data)
        info_record.set_additional_info(form.additional_info.data)
        info_record.set_name(form.name_surname.data)
        info_record.set_phone(form.phone.data)
        info_record.set_personal_account(form.personal_account.data)
        info_record.user_id = current_user.get_id()

        add_recording(form)
        db_sess.add(info_record)
        db_sess.commit()
        return redirect('/')

    return render_template('info.html', form=form)
