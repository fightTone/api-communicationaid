
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for,redirect,send_from_directory
from sqlalchemy import *
from models import *
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api/user/<acc_id>', methods=['GET'])
def getoneuser(acc_id):
    user = Account.query.filter_by(acc_id=acc_id).first()
    if not user:
        return jsonify({'message: "no user found"'})
    user_data = {}
    user_data['acc_id'] = user.acc_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['acc_type'] = user.acc_type
    return jsonify({'user': user_data})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token= request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing'}),
        try:
            data = jwt.decode(token), app.config['SECRET_KEY']
            current_user = Account.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args,**kwargs)
    return decorated

@app.route('/api/parent/editprofile/<int:acc_id>', methods=['POST']) #this api can also be used in editing other profiles(i.e teacher, child)
def update_parentinfo(acc_id):
# @token_required
	Parent.query.filter_by(acc_id=int(acc_id)).first()
	data = request.get_json()

	output = Parent(fname_p = data['fname_p'], lname_p = data['lname_p'], bday_p = data['bday_p'], add_p = data['add_p'])

	output = db.session.merge(output)
	db.session.add(output)
	db.session.commit()
	return jsonify({'message' : 'success!'})


@app.route('/api/signup', methods=['POST'])
def createuser():
	data = request.get_json()
	hashed_password = generate_password_hash(data['password'], method='sha256')
	new_acc = Account(acc_type=data['acc_type'], username = data['username'],email=data['email'], password = hashed_password)

	db.session.add(new_acc)
	db.session.commit()
	return jsonify({'message' : 'New user created.'})

@app.route('/api/login', methods=['POST'])
def login_api():

	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('un authenticated', 401, {'WWW-Authenticate' : 'Login required'})
	user = Account.query.filter_by(username=auth.username).first()

	if not user:
		return jsonify('User not found', 401, {'WWW-Authenticate' : 'Login required'})

	if check_password_hash(user.password,auth.password):
		token = jwt.encode({'account_id': Account.acc_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
		return jsonify({'status': 'ok', 'token': token.decode('UTF-8')})
	return make_response('Could not verify', {'WWW-Authenticate' : 'Login required'})

