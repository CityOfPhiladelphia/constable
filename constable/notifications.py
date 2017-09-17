from email.mime.text import MIMEText
import smtplib
import os

SMTP_CONNECTION = os.getenv('SMTP_CONNECTION')

# TODO: switch to notification service

def send_notification(notification, data):
    print(notification)
    print(data)
    # s = smtplib.SMTP(SMTP_CONNECTION) ## TODO: recycle?

    # # TODO: get base url
    # msg = MIMEText('Please follow this link to complete registration: {}'.format(token_str))

    # msg['Subject'] = 'City of Philadelphia Login Registration'
    # #msg['From'] = me
    # msg['To'] = registration.email

    # s.send_message(msg)
    
    # s.quit()
