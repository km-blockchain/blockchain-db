from hashlib import sha3_256

from app import app
from models import *
from flask import jsonify, request, abort, redirect, url_for


def trans_object(trans):
    return {'id': trans.id, 'from_id': trans.from_id, 'to_id':trans.to_id, 'amount':trans.amount, 'timestamp':trans.timestamp}

def block_to_hash(block):
    a = sha3_256()
    a.update(block.id.to_bytes(4, 'big'))
    a.update(ts(block.timestamp).to_bytes(8, 'big'))
    query = Transaction.query.filter_by(block_id=block.id).order_by(Transaction.id).all()
    for trans in query:
        a.update(trans.hash)
    return a.digest()


@app.route('/user')
def user():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify(id=user.id, name=user.name)


@app.route('/register')
def register():
    user = User(name=request.args['name'], password=request.args['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user', user_id=user.id))


@app.route('/trans')
def trans():
    trans = Transaction.query.filter_by(id=request.args['trans_id']).first()
    if not trans:
        return abort(404)
    return jsonify(trans_object(trans))


@app.route('/trans_from')
def trans_from():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify([trans_object(i) for i in user.from_trans])


@app.route('/trans_to')
def trans_to():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify([trans_object(i) for i in user.to_trans])


@app.route('/trans_add')
def trans_add():
    user = User.query.filter_by(id=request.args.get('from_id', None)).first()
    if user.password != request.args['password']:
        return abort(401)
    # user = User(name=request.args['name'], password=request.args['password'])
    trans = Transaction(from_id=request.args['from_id'], to_id=request.args['to_id'], amount=request.args['amount'])
    db.session.add(trans)
    db.session.commit()
    return redirect(url_for('trans', trans_id=trans.id))