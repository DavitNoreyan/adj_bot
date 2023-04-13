import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime


class Email:
    def __init__(self):
        self.smtp_server = 'smtp.mail.ru'
        self.smtp_port = 587
        self.message = MIMEMultipart()

    def send_mail(self, sender_email, sender_email_password, recipient_email, body_value):
        message = MIMEMultipart()
        now = datetime.datetime.now()
        formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
        message['Subject'] = 'Email From Bot About Changes'
        message['From'] = sender_email
        message['To'] = recipient_email
        body = f'There are change in {body_value} time is {formatted_date}!...'
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_email_password)
            server.sendmail(sender_email, recipient_email, message.as_string())


if __name__ == '__main__':
    sender_email = 'nordav@mail.ru'
    sender_password = 'Mu2LQbWdgktbiegJTuvP'
    recipient_email = 'davidnoreyan@gmail.com'
    body_value = 'Car'
    em = Email()
    em.send_mail(sender_email=sender_email, sender_email_password=sender_password, recipient_email=recipient_email,
                 body_value=body_value)
