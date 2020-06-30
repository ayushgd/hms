from hms import app
from datetime import datetime
from flask import render_template, session, url_for, request, redirect, flash, session, g
from .Forms import Login_form, Patient_create, Patient_delete, delete_result, Patient_update
from .Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
from .Config import db

# store patient ID for querying
pid = 0

# ==================================================================================
#                                   Home and Login
# ==================================================================================


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def main():
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    form = Login_form()
    if request.method == 'POST':
        # Validate the form
        if form.validate_on_submit():
            # Check the credentials
            if UserStore.query.filter_by(login=request.form.get('username'), password=request.form.get('password')).first():
                flash("Login successful", "success")
                session['user'] = request.form.get('username')
                return redirect(url_for('main'))
            else:
                flash("Invalid credentials", "danger")
                return render_template('login.html', title="Login", form=form)
    return render_template('login.html', title="Login", form=form)


@app.route("/index")
def index():
    return render_template("index.html")

# ==================================================================================
#                                 Patient Registration
# ==================================================================================


@app.route("/CreatePatient", methods=['GET', 'POST'])
def create_patient():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    # If form has been submitted
    form = Patient_create()
    if request.method == 'POST':
        if form.validate_on_submit():
            ssn_id = form.ssn_id.data
            name = form.patient_name.data
            age = form.patient_age.data
            date = form.date.data
            bed_type = form.Type_of_bed.data
            address = form.address.data
            state = request.form.get('stt')
            city = request.form.get('state_list')
            details = Patient_details(
                name, age, ssn_id, date, bed_type, address, city, state, status="Admitted")
            db.session.add(details)
            db.session.commit()
            flash("Patient creation initiated successfully", "success")
    return render_template("create_patient.html", title="Create Patient", form=form)


# ==================================================================================
#                                   Delete an existing patient
# ==================================================================================


@app.route("/DeletePatient", methods=["GET", "POST"])
def delete_patient():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    form = Patient_delete()
    if form.validate_on_submit():
        global pid
        pid = int(form.patient_id.data)
        patient = Patient_details.query.filter(
            Patient_details.id == int(form.patient_id.data))
        for patient_1 in patient:
            if patient_1:
                form2 = delete_result()
                flash("patient found", "success")
                return render_template("delete_patient2.html", title="Delete patient", patient=patient, form=form2)
        flash("patient not found", "danger")
    return render_template("delete_patient.html", title="Delete Patient", form=form)


@app.route("/deletepatient2", methods=["GET", "POST"])
def delete_patient2():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    form2 = delete_result()
    if form2.validate_on_submit():
        global pid
        print(pid)
        # delete query
        Patient_details.query.filter_by(id=pid).delete()
        db.session.commit()
        flash("patient deleted successfully", "success")

        return redirect(url_for('delete_patient'))
    else:
        flash("patient delete failed . Please try again", "danger")
        return redirect(url_for('delete_patient'))


# ==================================================================================
#                       Search for existing patient using Patient ID
# ==================================================================================


@app.route("/SearchPatient", methods=["GET", "POST"])
def search_patient():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    form = Patient_delete()
    if request.method == 'POST':
        if form.validate_on_submit():
            global pid
            pid = int(form.patient_id.data)
            patient = Patient_details.query.filter(
                Patient_details.id == int(form.patient_id.data))
            for patient_1 in patient:
                if patient_1:
                    flash("patient found", "success")
                    return render_template("search_patient.html", title="Search patient", patient=patient, form=form)
            flash("patient not found", "danger")
    return render_template("search_patient.html", title="Search Patient", form=form)


# ==================================================================================
#                    Update the detains of an existing patient
# ==================================================================================


@app.route("/UpdatePatient", methods=["GET", "POST"])
def update_patient():
    flag = 0
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    form = Patient_delete()
    if form.validate_on_submit():
        global pid
        pid = int(form.patient_id.data)
        patient = Patient_details.query.filter(
            Patient_details.id == int(form.patient_id.data))
        for patient_1 in patient:
            if patient_1:
                flash("patient found", "success")
                flag = 1
                form2 = Patient_update(Type_of_bed=patient_1.bed_type, date=patient_1.admission_date,
                                       address=patient_1.address, patient_name=patient_1.name, patient_age=patient_1.age)
                return render_template("update_patient.html", title="Update Patient", form=form, form2=form2, flag=flag, patient_s=patient)
        flash("Patient not found", "danger")
    return render_template("update_patient.html", title="Update Patient", form=form, flag=flag)


@app.route("/UpdatePatient2", methods=["GET", "POST"])
def update_result():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    form = Patient_update()
    if request.method == "POST":
        if form.validate_on_submit():
            global pid
            if request.form.get('stt') != "":
                if request.form.get('state_list') == None or request.form.get('state_list') == "":
                    patient = Patient_details.query.filter(
                        Patient_details.id == pid)
                    for patient_1 in patient:
                        if patient_1:

                            flag = 1
                            flash(
                                "You have to select city if you change state", "danger")
                            form2 = Patient_update(Type_of_bed=patient_1.bed_type, date=patient_1.admission_date,
                                                   address=patient_1.address, patient_name=patient_1.name, patient_age=patient_1.age)
                            return render_template("update_patient.html", title="Update Patient", form=form, form2=form2, flag=flag, patient_s=patient)

            print(pid)
            if request.form.get('stt') == "":
                name = form.patient_name.data
                age = form.patient_age.data
                date = form.date.data
                bed_type = form.Type_of_bed.data
                address = form.address.data

                Patient_details.query.filter_by(id=pid).update({"name": name})
                Patient_details.query.filter_by(
                    id=pid).update({"admission_date": date})

                Patient_details.query.filter_by(id=pid).update({"age": age})
                Patient_details.query.filter_by(
                    id=pid).update({"bed_type": bed_type})
                Patient_details.query.filter_by(
                    id=pid).update({"address": address})
            else:
                name = form.patient_name.data
                age = form.patient_age.data
                date = form.date.data
                bed_type = form.Type_of_bed.data
                address = form.address.data
                city = request.form.get('state_list')
                state = request.form.get('stt')
                Patient_details.query.filter_by(id=pid).update({"name": name})
                Patient_details.query.filter_by(
                    id=pid).update({"admission_date": date})
                Patient_details.query.filter_by(id=pid).update({"city": city})
                Patient_details.query.filter_by(
                    id=pid).update({"state": state})
                Patient_details.query.filter_by(id=pid).update({"age": age})
                Patient_details.query.filter_by(
                    id=pid).update({"bed_type": bed_type})
                Patient_details.query.filter_by(
                    id=pid).update({"address": address})

            db.session.commit()
            flash("Patient update intiated successfully ", "success")
            return redirect(url_for('update_patient'))
        patient = Patient_details.query.filter(Patient_details.id == pid)
        for patient_1 in patient:
            if patient_1:

                flag = 1
                flash(
                    "Please enter age in integer format and less than or equal to 3 digits in length", "danger")
                form2 = Patient_update(Type_of_bed=patient_1.bed_type, date=patient_1.admission_date,
                                       address=patient_1.address, patient_name=patient_1.name, patient_age=patient_1.age)
                return render_template("update_patient.html", title="Update Patient", form=form, form2=form2, flag=flag, patient_s=patient)


# ==================================================================================
#                   View all the admitted patients in record
# ==================================================================================


@app.route("/ViewAllPatients")
def view_patient():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect('login')
    patient = Patient_details.query.filter_by(status="Admitted")
    return render_template("view_patients.html", patients=patient)


# ==================================================================================
#                       Issue Medicines
# ==================================================================================


@app.route("/GetPatientDetails/Medicine", methods=["GET", "POST"])
def get_patient():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect(url_for('main'))
    form = Patient_delete()
    if request.method == 'POST':
        if form.validate_on_submit():
            global pid
            pid = int(form.patient_id.data)
            patient = Patient_details.query.filter(
                Patient_details.id == int(form.patient_id.data))
            for patient_1 in patient:
                if patient_1:
                    flash("patient found", "success")
                    return render_template("get_patient_details.html", title="Search patient", patient=patient)
            flash("patient not found", "danger")
    return render_template("get_patient_details.html", title="Get Patient Details", form=form)
    

@app.route("/IssueMedicine", methods=["GET", "POST"])
def issue_medicine():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect(url_for('main'))
        
    global pid
    pid = request.form.get('pid')
    print(pid)
    if Patient_Medicine.query.filter(Patient_Medicine.patient_id==pid)== None:
        print("check null")
    medicine = Patient_Medicine.query.filter(Patient_Medicine.patient_id==pid)
    print(medicine)
    return render_template("issue_medicine.html", pid=pid, medicine=medicine)

# ==================================================================================
#                                 Delete the user Session
# ==================================================================================


@app.route("/logout")
def logout():
    # Remove user from the session
    if session['user']:
        session['user'] = None
        return redirect(url_for('main'))
