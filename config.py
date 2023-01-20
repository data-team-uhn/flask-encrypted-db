import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def read_secret(variable, default=''):
    secrets_path = os.getenv('SECRETS_PATH', '/run/secrets')
    secret_file = Path(os.path.join(secrets_path, variable))
    if secret_file.is_file():
        return secret_file.read_text().replace('\n', '')
    else:
        return os.getenv(variable, default)


class Config(object):
    """
    The base config. All shared config values are kept here.
    """

    # Load all environment variables first
    load_dotenv()

    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    MAX_REGISTRATION_ATTEMPTS = 5
    ENV = os.getenv('ENV')
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 26214400  # 25 mb

    # DB connection setup
    db_user = os.getenv('POSTGRES_USER')
    db_pass = read_secret('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST') + ':' + str(os.getenv('POSTGRES_PORT'))
    db_name = os.getenv('POSTGRES_DB')

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "max_overflow": 25,
        "pool_size": 25,
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_name)

    # Secret used to encrypt db-fields
    POSTGRES_SECRET_KEY = read_secret('POSTGRES_SECRET_KEY')

    # Get key for hashing passwords and user data
    SECRET_KEY = str.encode(read_secret('SECRET_KEY'))


class DevConfig(Config):
    PREFERRED_URL_SCHEME = 'http'


class TestConfig(Config):
    PREFERRED_URL_SCHEME = 'http'


class ProdConfig(Config):
    PREFERRED_URL_SCHEME = 'https'


configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'staging': ProdConfig,
    'production': ProdConfig,
}

config = configs[Config.ENV]
