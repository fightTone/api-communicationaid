
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
    user_data = {}                          #container
    user_data['acc_id'] = user.acc_id
    user_data['username'] = user.username  #dictionary
    user_data['email'] = user.email
    user_data['acc_type'] = user.acc_type
    return jsonify({'user': user_data})

@app.route('/api/educational/progress/', methods=['POST'])
def progress(ed_num):
    report = Progress.query.filter_by(ed_num=ed_num).first()

    prog_data = {}
    prog_data['title'] = report.title
    prog_data['details'] = report.details
    prog_data['score'] = report.score

    db.session.add(Progress)
    db.session.commit()
    return jsonify({'data': prog_data, 'status': 'ok'})
