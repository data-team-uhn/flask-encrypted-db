from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)


# Set up db environment
db = SQLAlchemy()


# Import models
from .users import *
