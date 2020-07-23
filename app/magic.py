import secrets

from flask import jsonify, abort, request, render_template

from app.db import app, db
from app.models import User


@app.route('/')
def hello():
    urls = [user.full_link for user in User.query.order_by(User.username).all()]
    return render_template('page.html', urls=urls)


@app.route('/magic/api/v1.0/users', methods=['GET'])
def get_users():
    users = [user.get_security_payload() for user in User.query.order_by(User.username).all()]
    return jsonify(users)


@app.route('/magic/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.get_security_payload())


@app.route('/magic/api/v1.0/users/<int:user_id>/reset-link', methods=['GET'])
def user_reset_link(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    user.counter = 0
    user.secure = secrets.token_urlsafe(16)
    db.session.commit()
    return jsonify(user.get_security_payload())


@app.route('/magic/api/v1.0/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/magic/api/v1.0/magic/<string:magic_id>', methods=['GET'])
def use_magic(magic_id):
    user = User.query.filter_by(secure=magic_id).first_or_404()
    if not user:
        abort(404)
    user.counter = User.counter + 1
    db.session.commit()
    return jsonify(user.get_security_payload())
