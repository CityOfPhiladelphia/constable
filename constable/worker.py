from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib
import os

from sqlalchemy import text
from sqlalchemy.sql.expression import exists

from .models import Registration, User, Token

SMTP_CONNECTION = os.getenv('SMTP_CONNECTION')

registration_sql = """
WITH nextRegisrations as (
    SELECT id, status
    FROM registrations
    WHERE
        attempts < 3 AND
        (status = 'new' OR
          (status = 'processing' AND (:now > (locked_at + INTERVAL '1 second' * 600))) OR
          (status = 'retry' AND (:now > (locked_at + INTERVAL '1 second' * 600))))
    ORDER BY
        created_at
    LIMIT 10
    FOR UPDATE SKIP LOCKED
)
UPDATE registrations SET
    status = 'processing'::registration_statuses,
    worker_id = :worker_id,
    locked_at = :now,
    attempts = attempts + 1
FROM nextRegisrations
WHERE registrations.id = nextRegisrations.id
RETURNING registrations.*;
"""

def pull_registrations(session, now, worker_id):
    return session.query(Registration)\
        .from_statement(text(registration_sql))\
        .params(now=now, worker_id=worker_id)\
        .all()

def run(session, worker_id, now=None):
    if now == None:
        now = datetime.utcnow()

    registrations = pull_registrations(session, now, worker_id)

    #s = smtplib.SMTP(SMTP_CONNECTION)

    for registration in registrations:
        user_exists = session.query(exists().where(User.email == registration.email)).scalar()
        ## TODO: check for loginless User? eg just email
        if user_exists:
            registration.status = 'email_already_registered'
            session.commit()
        else:
            token = Token(
                type='token',
                scopes=['registration'],
                expires_at=datetime.utcnow() + timedelta(days=5),
                ip=registration.ip,
                user_agent=registration.user_agent)
            session.add(token)
            session.commit()

            token_str = token.token

            print(registration.id)
            print(token_str)

            ## TODO: switch to notification service

            ## TODO: get base url
            # msg = MIMEText('Please follow this link to complete registration: {}'.format(token_str))

            # msg['Subject'] = 'City of Philadelphia Login Registration'
            # #msg['From'] = me
            # msg['To'] = registration.email

            # s.send_message(msg)

            registration.status = 'verification_email_sent'
            registration.verification_token_id = str(token.id)
            session.commit()
    
    # s.quit()

    ## TODO: hit cloudwatch here or in cli.py ?
