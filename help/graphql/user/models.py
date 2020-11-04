from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from numpy.core import unicode
from sqlalchemy import ForeignKey

from core import db


class PrimaryKeyIdMixin(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)



class User(PrimaryKeyIdMixin):
    ''' A model for storing data pulled from random user '''
    __tablename__ = 'user'
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    username = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User {} {}>'.format(self.firstname, self.lastname)

