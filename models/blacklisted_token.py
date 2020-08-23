from datetime import datetime

from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField


class BlacklistedToken(Document):
    jti = StringField(required=True, unique=True)
    created_at = DateTimeField(required=False, default=datetime.utcnow)
    updated_at = DateTimeField(required=False, default=datetime.utcnow)
