import os
from hms import app

app = Flask(__name__)
app.secret_key = os.urandom(24)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hospitalMS"

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)