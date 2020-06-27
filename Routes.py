from hms import app
from flask import render_template, session, url_for, request, redirect, flash
from .Forms import Login_form

@app.route("/",methods=["GET","POST"])
def main():
    form=Login_form()
    if form.validate_on_submit():
        flash("login successful")
        return redirect(url_for('index'))

    return render_template('login.html', title="Login", form=form)

@app.route("/index")
def index():
    return render_template("index.html")