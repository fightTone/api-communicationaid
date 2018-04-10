
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



@app.route('/api/signup', methods=['POST'])
def createuser():
	data = request.get_json()
	hashed_password = generate_password_hash(data['password'], method='sha256')
	new_acc = Account(acc_type=data['acc_type'], username = data['username'],email=data['email'], password = hashed_password)

	db.session.add(new_acc)
	db.session.commit()
	return jsonify({'message' : 'New user created.'})



