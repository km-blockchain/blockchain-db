from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=0)
    from_trans = db.relationship('Transaction', foreign_keys='Transaction.from_id', backref='from_user')
    to_trans = db.relationship('Transaction', foreign_keys='Transaction.to_id', backref='to_user')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.Datetime, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)