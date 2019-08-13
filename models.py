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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    hash = db.Column(db.LargeBinary(32))
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'))


class Block(db.Model):
    __tablename__ = 'blocks'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    hash = db.Column(db.LargeBinary(32))
    is_verified = db.Column(db.Boolean, default=False)
    previous_hash = db.Column(db.LargeBinary(32), default=b'\x00' * 32)
    trans = db.relationship(Transaction, backref='block')
    users = db.relationship(User, secondary='verifications', backref='blocks')


class Verification(db.Model):
    __tablename__ = 'verifications'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

