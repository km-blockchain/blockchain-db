from app import app
from models import *
from flask import jsonify, request, abort


def trans_object(trans):
    return {'id': trans.id, 'from_id': trans.from_id, 'to_id':trans.to_id, 'amount':trans.amount, 'timestamp':trans.timetamp}


@app.route('/user')
def user():
    user = User.query.filter_by(id=request.args.get('user_id', None)).first()
    if not user:
        return abort(404)
    return jsonify(id=user.id, name=user.name)


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