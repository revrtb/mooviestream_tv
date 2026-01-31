from lib.database import db
from datetime import datetime

class Link(db.Model):
    """Link"""

    __tablename__ = 'link'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.VARCHAR(1000), index=True)
    short_code = db.Column(db.VARCHAR(100), unique=True, index=True, default=None)
    custom_code = db.Column(db.VARCHAR(100), unique=True, index=True, default=None)
    description = db.Column(db.VARCHAR(1000), default=None)
    expire_after = db.Column(db.DateTime, default=None)
    is_custom = db.Column(db.Boolean, default=False)
    is_disabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    last_call = db.Column(db.DateTime)
    userId = db.Column(db.Integer)
    brandId = db.Column(db.Integer)

    def __init__(self, url):
        self.url = url
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_call = datetime.now()


