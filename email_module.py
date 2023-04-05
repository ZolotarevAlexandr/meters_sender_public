import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging


def send_counters_info(counters_record):
    try:
        sender_email = "Zolotarev10032006@yandex.ru"
        receiver_email = "andzolotarev@yandex.ru"
        password = "skywjdajgsbvlgdr"

        message = MIMEMultipart("alternative")
        message["Subject"] = f"Показания счётчиков за {counters_record.date.strftime('%d.%m.%Y')}"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = str(counters_record)

        html = f"""\
        <html>
            <body>
                <p>
                Дата: {counters_record.date.strftime('%d.%m.%Y')} <br>
                Кухня, горячая вода: {counters_record.kitchen_hot} <br>
                Кухня, холодная вода: {counters_record.kitchen_cold} <br>
                Ванная, горячая вода: {counters_record.bathroom_hot} <br>
                Ванная, холодная вода: {counters_record.bathroom_cold} <br>
                Электричество: {counters_record.electricity} <br>
                </p>
            </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        logging.debug('[email_module.py, send_counters_info] Email generated')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.yandex.ru", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        logging.info(f'[email_module.py, send_counters_info] Email to {receiver_email} successfully sent')
    except Exception as e:
        logging.error(f' [email_module.py, send_counters_info]'
                      f'While sending a message an error occurred: {e}', exc_info=True)
