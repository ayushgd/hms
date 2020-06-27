from hms import app
from flask import render_template, session, url_for, request, redirect, flash, session
from .Forms import Login_form
from Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def main():
    form=Login_form()
    if request.method == 'POST':
        #Validate the form
        if form.validate_on_submit():
            #Check the credentials
            if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
                flash("login successful")
                #g.user = "Admin"
                session['username'] = request.form.get('username')
                return render_template('create_patient.html', alert='success', title="Login", form=form)
            else:
                flash("login failed")
                return render_template('login.html', alert='failed', title="Login", form=form)
    return render_template('login.html', title="Login", form=form)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/CreatePatient")
def create_patient():
    if not session["username"]:
        return redirect('login')
    return render_template("create_patient.html", title="Create Patient")

@app.route("/DeletePatient")
def delete_patient():
    if not session["username"]:
        return redirect('login')
    return render_template("delete_patient.html", title="Delete Patient")

@app.route("/UpdatePatient")
def update_patient():
    if not session["username"]:
        return redirect('login')
    return render_template("update_patient.html", title="Update Patient")


@app.route("/logout")
def logout():
    session['username'] = None
    return redirect(url_for('main'))