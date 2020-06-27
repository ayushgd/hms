from flask import Flask, render_template, session, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def main():
    return render_template('index.html')