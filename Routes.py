from hms import app
from datetime import datetime
from flask import render_template, session, url_for, request, redirect, flash, session
from .Forms import Login_form
from .Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
from .Config import db



@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def main():
    if session.get('username'):
        return render_template('index.html', user=session['username'])
    form = Login_form()
    if request.method == 'POST':
        # Validate the form
        if form.validate_on_submit():
            # Check the credentials
            if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
                flash("login successful")
                #g.user = "Admin"
                session['username'] = request.form.get('username')
                return redirect(url_for('create_patient'))
            else:
                return render_template('login.html', alert='failed', title="Login", form=form)
    return render_template('login.html', title="Login", form=form)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/CreatePatient", methods=['GET', 'POST'])
def create_patient():
    if 'username' not in session or not session['username']:
        return redirect('login')
    # If form has been submitted
    if request.method == 'POST':
        ssn_id = request.form.get('ssn_id')
        name = request.form.get('patient_name')
        age = int(request.form.get('patient_age'))
        date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        bed_type = request.form.get('bed')
        address = request.form.get('address')
        state = request.form.get('state_list')
        city = request.form.get('stt')
        #create_p([ssn_id, name, age, date, bed_type, address, state, city])
        details = Patient_details(
            name, age, ssn_id, date, bed_type, address, city, state, status="Admitted")
        db.session.add(details)
        db.session.commit()
        flash("Succefully Created")
    return render_template("create_patient.html", title="Create Patient")


@app.route("/DeletePatient")
def delete_patient():
    if 'username' not in session:
        return redirect('login')
    return render_template("delete_patient.html", title="Delete Patient")


@app.route("/UpdatePatient")
def update_patient():
    if 'username' not in session:
        return redirect('login')
    return render_template("update_patient.html", title="Update Patient")


@app.route("/logout")
def logout():
    if session['username']:
        #return render_template('index.html', user=session['username'])
        session['username'] = None
        return redirect(url_for('main'))
