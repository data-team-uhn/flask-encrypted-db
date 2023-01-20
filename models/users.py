import uuid
import sqlalchemy as sa
from config import config
from . import db, TimestampMixin
from sqlalchemy_utils import EncryptedType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


class Users(db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False)
    email = db.Column(EncryptedType(sa.Unicode, config.POSTGRES_SECRET_KEY, AesEngine, 'pkcs5'), nullable=False)
