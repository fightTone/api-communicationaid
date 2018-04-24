from flask import Flask, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from config import dbstring
from flask_compress import Compress


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:walakokahibaw@localhost/db'
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mail = Mail(app)
Compress(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from models import Account

def createTables():
	db.create_all()

createTables()	
app.debug = True
