from datetime import datetime

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