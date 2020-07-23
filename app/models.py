from datetime import datetime

from app.db import db, app


class User(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    secure = db.Column(db.String(140), index=True, unique=True)  # magic url
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    counter = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def full_link(self):
        if self.secure:
            return f'{app.config["HOSTNAME"]}/magic/api/v1.0/magic/{self.secure}'

    # Custom User Payload
    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email,
            'code': self.secure,
            'counter': self.counter,
            'url': self.full_link,
        }
