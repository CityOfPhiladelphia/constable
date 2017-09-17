from datetime import datetime, timedelta
import os

from sqlalchemy import text
from sqlalchemy.sql.expression import exists

from .models import Registration, User, Token, RecoverPasswordRequest
from .notifications import send_notification

WORKER_TIMEOUT = int(os.getenv('WORKER_TIMEOUT', 600))
WORKER_RETRY_INTERVAL = int(os.getenv('WORKER_RETRY_INTERVAL', 600))

worker_pull_sql = """
WITH nextItems as (
    SELECT id
    FROM {table_name}
    WHERE
        attempts < 3 AND
        (status = 'new' OR
          (status = 'processing' AND (:now > (locked_at + INTERVAL '1 second' * {timeout}))) OR
          (status = 'retry' AND (:now > (locked_at + INTERVAL '1 second' * {retry_interval}))))
    ORDER BY
        created_at
    LIMIT 10
    FOR UPDATE SKIP LOCKED
)
UPDATE {table_name} SET
    status = 'processing'::{status_enum_name},
    worker_id = :worker_id,
    locked_at = :now,
    attempts = attempts + 1
FROM nextItems
WHERE {table_name}.id = nextItems.id
RETURNING {table_name}.*;
"""

def get_pull_sql(model):
    table_name = model.__tablename__
    status_enum_name = table_name[:-1] + '_statuses'
    return worker_pull_sql.format(
        table_name=table_name,
        status_enum_name=status_enum_name,
        timeout=WORKER_TIMEOUT,
        retry_interval=WORKER_RETRY_INTERVAL)

def pull_tasks(session, model, now, worker_id):
    return session.query(model)\
        .from_statement(text(get_pull_sql(model)))\
        .params(now=now, worker_id=worker_id)\
        .all()

## TODO: publish registration success metric

def process_registrations(now, session, registrations):
    for registration in registrations:
        try:
            user_exists = session.query(exists().where(User.email == registration.email)).scalar()
            ## TODO: check for loginless User? eg just email
            if user_exists:
                ## TODO: send email "Did you forget you account existed? ... link to reset password"
                ## TODO: if a registration with the same email has been used in the last 12 or 24 hours,
                ##       do not send another email. Prevents someone's email from being remote pounded
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

                send_notification('registration', {
                    'email': registration.email,
                    'data': {
                        'first_name': registration.first_name,
                        'last_name': registration.last_name,
                        'token': token_str
                    }
                })

                registration.status = 'verification_email_sent'
                registration.verification_token_id = str(token.id)
                session.commit()
        except Exception as e:
            print(e)
            ## TODO: use logger
            ## TODO: publish registration failure cloudwatch metric

## TODO: publish recovery success metric

def process_password_recovery_requests(now, session, password_recovery_requests):
    for password_recovery_request in password_recovery_requests:
        try:
            pass
        except Exception as e:
            print(e)
            ## TODO: use logger
            ## TODO: publish registration failure cloudwatch metric

def run(session, worker_id, now=None):
    if now == None:
        now = datetime.utcnow()

    ## TODO: if each of the below is 10, keep iterating and control rate?

    registrations = pull_tasks(session, Registration, now, worker_id)
    process_registrations(now, session, registrations)

    password_recovery_requests = pull_tasks(session, RecoverPasswordRequest, now, worker_id)
    process_password_recovery_requests(now, session, password_recovery_requests)

    ## TODO: hit cloudwatch here or in cli.py ?
