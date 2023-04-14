import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from encryption_module import decrypt_info
from data import db_session
from data.user_info_model import UserInfo
import logging


def send_counters_info(current_record, previous_record, user):
    try:
        db_sess = db_session.create_session()
        user_info = db_sess.query(UserInfo).filter(UserInfo.user_id == user.get_id()).first()
        sender_email = user.login
        receiver_email = user_info.receiver_email
        password = decrypt_info(user_info.hashed_mail_app_password)

        additional_info = decrypt_info(user_info.additional_info)
        name = decrypt_info(user_info.name_surname)
        phone = decrypt_info(user_info.phone)
        personal_account = decrypt_info(user_info.personal_account)

        kitchen_hot_serial = user_info.kitchen_hot_serial
        kitchen_cold_serial = user_info.kitchen_cold_serial
        bathroom_hot_serial = user_info.bathroom_hot_serial
        bathroom_cold_serial = user_info.bathroom_cold_serial
        electricity_serial = user_info.electricity_serial

        message = MIMEMultipart("alternative")
        message["Subject"] = f'Показания счетчиков по лицевому счету {personal_account} за ' \
                             f'{current_record.date.strftime("%m.%Y")}'
        message["From"] = sender_email
        message["To"] = receiver_email

        text = str(current_record)

        html = f"""\
        <html>
            <body>
                <pre>
Здравствуйте!
Информация о показаниях приборов учета за {current_record.date.strftime('%m.%Y')}
{additional_info}

Виды услуг                      Серийный №              Показания

Горячее водоснабжение (кухня)	{kitchen_hot_serial}    {current_record.kitchen_hot - previous_record.kitchen_hot}
Горячее водоснабжение (с/у)     {bathroom_hot_serial}   {current_record.bathroom_hot - previous_record.kitchen_hot}
Холодное водоснабжение (кухня)	{kitchen_cold_serial}   {current_record.kitchen_hot - previous_record.kitchen_hot}
Холодное водоснабжение (с/у)	{bathroom_cold_serial}  {current_record.bathroom_cold - previous_record.kitchen_hot}
Электроэнергия	                {electricity_serial}    {current_record.electricity - previous_record.kitchen_hot}

{name}
{phone}
                </pre>
            </body>
        </html>
                """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        logging.debug(f'[email_module.py, send_counters_info] Email from {sender_email} generated')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.yandex.ru", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        logging.info(f'[email_module.py, send_counters_info] '
                     f'Email from {sender_email} to {receiver_email} successfully sent')
        return True
    except Exception as e:
        logging.error(f' [email_module.py, send_counters_info]'
                      f'While sending a message an error occurred: {e}', exc_info=True)
        return False
