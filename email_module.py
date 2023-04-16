import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from encryption_module import decrypt_info
import logging


STYLE = 'pre {white-space: pre}'


def send_counters_info(current_record, user):
    try:
        sender_email = user.login
        receiver_email = user.user_info[0].receiver_email
        password = decrypt_info(user.user_info[0].hashed_mail_app_password)
        email_server = user.user_info[0].email_server

        additional_info = decrypt_info(user.user_info[0].additional_info)
        name = decrypt_info(user.user_info[0].name_surname)
        phone = decrypt_info(user.user_info[0].phone)
        personal_account = decrypt_info(user.user_info[0].personal_account)

        kitchen_hot_serial = user.user_info[0].kitchen_hot_serial
        kitchen_cold_serial = user.user_info[0].kitchen_cold_serial
        bathroom_hot_serial = user.user_info[0].bathroom_hot_serial
        bathroom_cold_serial = user.user_info[0].bathroom_cold_serial
        electricity_serial = user.user_info[0].electricity_serial

        meters = current_record.get_all()

        message = MIMEMultipart("alternative")
        message["Subject"] = f'Показания счетчиков по лицевому счету {personal_account} за ' \
                             f'{current_record.date.strftime("%m.%Y")}'
        message["From"] = sender_email
        message["To"] = receiver_email

        text = str(current_record)

        html = f"""\
        <html>
        <style>
        {STYLE}
        </style>
            <body>
                <blockquote>                
                <pre>
Здравствуйте!
Информация о показаниях приборов учета за {current_record.date.strftime('%m.%Y')}
{additional_info}

Виды услуг                      Серийный №\tПоказания
                                                
Горячее водоснабжение (кухня)   {kitchen_hot_serial}\t\t{meters[0]}
Холодное водоснабжение (кухня)  {kitchen_cold_serial}\t\t{meters[1]}
Горячее водоснабжение (с/у)     {bathroom_hot_serial}\t\t{meters[2]}
Холодное водоснабжение (с/у)    {bathroom_cold_serial}\t\t{meters[3]}
Электроэнергия                  {electricity_serial}\t\t{meters[4]}

{name}
{phone}
                </pre>
                </blockquote>
            </body>
        </html>
                """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        logging.debug(f'[email_module.py, send_counters_info] Email from {sender_email} generated')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(email_server, 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        logging.info(f'[email_module.py, send_counters_info] '
                     f'Email from {sender_email} to {receiver_email} successfully sent')
        return True
    except Exception as e:
        logging.error(f' [email_module.py, send_counters_info]'
                      f'While sending a message an error occurred: {e}', exc_info=True)
        return False
