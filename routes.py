from app import app
from models import *
from flask import jsonify, request, abort


@app.route('/user')
def user():
    user = User.query.filter_by(id=request.args['user_id']).first()
    if not user:
        return abort(404)
    return jsonify(id=user.id, name=user.name)
@app.route('/trans')
def trans():
    trans = Transaction.querty.filter_by(id=request.args['trans_id']).first()
    if not user:
        return abort(404)
    return jsonify(trans_object(trans))
