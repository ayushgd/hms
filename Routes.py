from hms import app
from flask import render_template, session, url_for, request, redirect, flash
from .Forms import Login_form

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def main():
    form=Login_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.username)
            print(form.password)
            if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
                flash("login successful")
                return render_template('index.html', alert='success')
            else:
                flash("login failed")
                return render_template('index.html', alert='failed')
    return render_template('login.html', title="Login", form=form)

@app.route("/index")
def index():
    return render_template("index.html")