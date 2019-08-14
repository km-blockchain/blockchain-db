from hashlib import sha3_256
from app import app
from models import *
from flask import jsonify, request, abort, redirect, url_for


def trans_object(trans):
    return {'id': trans.id, 'from_id': trans.from_id, 'to_id': trans.to_id, 'amount': trans.amount,
            'timestamp': trans.timestamp, 'hash': (trans.hash or b'\x00').hex()}


def block_object(block):
    return {'id': block.id, 'timestamp': block.timestamp, 'hash': block.hash.hex(),
            'previous_hash': block.previous_hash.hex(), 'is_verified': block.is_verified}


def block_to_hash(block):
    a = sha3_256()
    a.update(block.id.to_bytes(4, 'big'))
    a.update(ts(block.timestamp).to_bytes(8, 'big'))
    query = Transaction.query.filter_by(block_id=block.id).order_by(Transaction.id).all()
    for trans in query:
        a.update(bytes(trans.hash))
    a.update(bytes(block.previous_hash))
    return a.digest()


def trans_to_hash(trans):
    a = sha3_256()
    a.update(trans.id.to_bytes(4, 'big'))
    a.update(trans.from_id.to_bytes(4, 'big'))
    a.update(trans.to_id.to_bytes(4, 'big'))
    a.update(ts(trans.timestamp).to_bytes(8, 'big'))
    a.update(fl(trans.amount).to_bytes(8, 'big'))
    return a.digest()


def ts(timestamp):
    return int(timestamp.timestamp())


def fl(number):
    return hash(number) % 2**64


@app.route('/user')
def user():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify(id=user.id, name=user.name, balance=user.balance)


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
    query = Transaction.query.filter_by(block_id=None).all()
    count = len(query)
    if count == 4:
        block = Block()
        db.session.add(block)
        db.session.commit()
        block.previous_hash = bytes(Block.query.get(block.id - 1).hash)
        for trans in query:
            trans.block_id = block.id
            trans.hash = trans_to_hash(trans)
            block.hash = block_to_hash(block)
        db.session.commit()
    return redirect(url_for('trans', trans_id=trans.id))


@app.route('/verify_block')
def verify_block():
    user = User.query.filter_by(id=request.args['user_id']).first()
    block = Block.query.filter_by(id=request.args['block_id']).first()
    verify = Verification.query.filter_by(user_id=request.args['user_id'],
                                          block_id=request.args['block_id']).first()
    if block.is_verified or verify:
        return jsonify(success=True)
    if user.password != request.args['password']:
        return abort(401)
    verify = Verification(user_id=user.id, block_id=request.args['block_id'])
    db.session.add(verify)
    if Verification.query.filter_by(block_id=request.args['block_id']).count() == 4:
        block.is_verified = True
        for trans in block.trans:
            if trans.amount > trans.from_user.balance:
                continue
            trans.from_user.balance -= trans.amount
            trans.to_user.balance += trans.amount
    db.session.commit()
    return jsonify(success=True)


@app.route('/block_get')
def block_get():
    block = Block.query.filter_by(id=request.args['block_id']).first()
    if not block:
        return abort(404)
    return block_object(block)


@app.route('/verify_get')
def verify_get():
    user = User.query.filter_by(id=request.args['user_id']).first()
    block = Block.query.filter_by(is_verified=False).order_by(Block.id).first()
    if not block:
        return jsonify({})
    verify = Verification.query.filter_by(user_id=request.args['user_id'],
                                          block_id=block.id).first()
    if verify:
        return jsonify({})
    return redirect(url_for('block_get', block_id=block.id))


@app.route('/login')
def login():
    user = User.query.filter_by(name=request.args['name']).first()
    if user.password != request.args['password']:
        return abort(401)
    return redirect(url_for('user', user_id=user.id))
