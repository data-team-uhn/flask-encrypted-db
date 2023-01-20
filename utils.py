import hashlib
import binascii
from models import *
from flask import Flask
from config import config
from flask.json import JSONEncoder
# import sqlalchemy.ext.declarative.api
import sqlalchemy.orm.decl_api

# Create a fake Flask app to enable Flask-SQLAlchemy to behave as expected
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# Push fake app context so that db can run queries
app.app_context().push()


class CustomJsonEncoder(JSONEncoder):
    def default(self, x):
        if isinstance(x, datetime):
            return x.astimezone().isoformat()
        elif isinstance(x, UUID):
            return str(x)
        elif isinstance(type(x), sqlalchemy.orm.decl_api.DeclarativeMeta):
            return {key: getattr(x, key) for key in x.__dict__.keys() if key not in ['_sa_instance_state']}
        else:
            return super().default(x)


def hash_pwd(pwd):
    salt = config.SECRET_KEY
    """Return a hashed password."""
    pwdhash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt, 100000)).decode('ascii')
    return pwdhash


def initiate_db():
    db.session.commit()

    # Attempt to drop all tables and re-create them
    try:
        db.drop_all()
    except:
        pass

    db.create_all()
    db.session.commit()
    db.session.flush()


def create_admin_user():
    user = Users(
        username="admin",
        user_type="admin",
        email="admin@example.com",
        password=hash_pwd("password"),
    )
    db.session.add(user)
    db.session.commit()


json = CustomJsonEncoder()
