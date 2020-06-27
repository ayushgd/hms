from hms import app
from flask import render_template, session, url_for, request, redirect

@app.route("/")
def main():
    return render_template('login.html', title="Login")