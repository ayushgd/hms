import os
from hms import app

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hospitalMS"

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)