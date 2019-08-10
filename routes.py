from app import app
from models import *
from flask import jsonify, request, abort, redirect, url_for


def trans_object(trans):
    return {'id': trans.id, 'from_id': trans.from_id, 'to_id':trans.to_id, 'amount':trans.amount, 'timestamp':trans.timetamp}


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
    return redirect(url_for('user'))


@app.route('/trans')
def trans():
    trans = Transaction.querty.filter_by(id=request.args['trans_id']).first()
    if not user:
        return abort(404)
    return jsonify(trans_object(trans))


@app.route('/trans_from')
def trans_from():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify(*[trans_object(i) for i in user.from_trans])


@app.route('/trans_to')
def trans_to():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify(*[trans_object(i) for i in user.to_trans])