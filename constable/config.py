import os

from cryptography.fernet import Fernet

CSRF_SECRET = os.getenv('CSRF_SECRET', Fernet.generate_key())
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/constable_test')
TOKEN_SECRET = os.getenv('TOKEN_SECRET', Fernet.generate_key())
BASE_URL = os.getenv('BASE_URL', '')
GOOGLE_RECAPTCHA_SECRET = os.getenv('GOOGLE_RECAPTCHA_SECRET')
NUMBER_OF_PROXIES = int(os.getenv('NUMBER_OF_PROXIES', 0))
