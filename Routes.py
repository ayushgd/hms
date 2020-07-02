from hms import app
from datetime import datetime
from flask import render_template, session, url_for, request, redirect, flash, session, g
from .Forms import Login_form, Patient_create, Patient_delete, delete_result, Patient_update
from .Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
from .Config import db

# store patient ID for querying
pid = 0

#Function to implement session management and check the category of stakeholder accessing the website
def check_session():
    if 'user' not in session or not session['user']:
        return None
    else:
        stakeholder_type = session['user'][-1]
        if stakeholder_type == 'A':
            session['stakeholder'] = 'registration_desk_executive'
            return 'registration_desk_executive'
        elif stakeholder_type == 'D':
            session['stakeholder'] = 'diagnostic_executive'
            return 'diagnostic_executive'
        elif stakeholder_type == 'P':
            session['stakeholder'] = 'pharmacy_executive'
            return 'pharmacy_executive'

# ==================================================================================
#                                   Home and Login
# ==================================================================================


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def main():
    if check_session():
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
    if not check_session():
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))
    return render_template("index.html")

# ==================================================================================
#                                 Patient Registration
# ==================================================================================


@app.route("/CreatePatient", methods=['GET', 'POST'])
def create_patient():

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

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
#                              Delete an existing patient
# ==================================================================================


@app.route("/DeletePatient", methods=["GET", "POST"])
def delete_patient():

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

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

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

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

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
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
                    return render_template("search_patient.html", title="Search patient", patient=patient, form=form)
            flash("patient not found", "danger")
    return render_template("search_patient.html", title="Search Patient", form=form)


# ==================================================================================
#                    Update the detains of an existing patient
# ==================================================================================


@app.route("/UpdatePatient", methods=["GET", "POST"])
def update_patient():
    flag = 0

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

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

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

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

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

    patient = Patient_details.query.filter_by(status="Admitted")
    return render_template("view_patients.html", patients=patient)


# ==================================================================================
#                                   Issue Medicines
# ==================================================================================


@app.route("/GetPatientDetails/Medicine", methods=["GET", "POST"])
def get_patient():

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive' and check_session()!= 'pharmacy_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
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
                    medicine=med_patient(patient_1)
                    if medicine!=None:
                    
                        return render_template("get_patient_details.html", title="Search patient", patient=patient,medicine=medicine.all())
                    else:
                        return render_template("get_patient_details.html",title="Search patient",patient=patient)
            flash("patient not found", "danger")
    return render_template("get_patient_details.html", title="Get Patient Details", form=form)
    

@app.route("/IssueMedicine", methods=["GET", "POST"])
def issue_medicine():
    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive' and check_session()!= 'pharmacy_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

    global pid
    pid = request.form.get('pid')
    print(pid)
    if Patient_Medicine.query.filter(Patient_Medicine.patient_id==pid)== None:
        print("check null")
    medicine = Patient_Medicine.query.filter(Patient_Medicine.patient_id==pid)
    print(medicine)
    return render_template("issue_medicine.html", pid=pid, medicine=medicine)

def med_patient(patient):
    mid=patient.id
    if Patient_Medicine.query.filter(Patient_Medicine.patient_id==mid).first()==None:
        return None
    else:
        x=Patient_Medicine.query.join(Medicine,Patient_Medicine.medicine_id==Medicine.id).filter(Patient_Medicine.patient_id==mid)
        return x
# ==================================================================================
#                                   Diagnostics
# ==================================================================================


@app.route("/GetPatientDetails/Diagnostics", methods=["GET", "POST"])
def patient_diagnosis():

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive' and check_session()!= 'diagnostic_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
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
                    return render_template("get_patient_diagnosis.html", title="Search patient", patient=patient, pid=pid)
            flash("patient not found", "danger")
    return render_template("get_patient_diagnosis.html", title="Get Patient Diagnostics", form=form)
    

@app.route("/Diagnostics", methods=["GET", "POST"])
def diagnostics():

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive' and check_session()!= 'diagnostic_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

    global pid
    pid = request.form.get('pid')
    return render_template("diagnostics.html", pid=pid, title="Conduct Diagnostics")


# ==================================================================================
#                                   Patient Billing
# ==================================================================================

@app.route('/FinalBilling', methods=["GET", "POST"])
def billing():

    # Check that an authorised user only can access this functionality
    if check_session()!='registration_desk_executive':
        flash('You are not authorised to access that! Please login with proper credentials.', 'danger')
        return redirect(url_for('main'))

    form = Patient_delete()
    if request.method == 'POST':
        patient = Patient_details.query.filter(Patient_details.id == int(form.patient_id.data))
        for patient_1 in patient:
            if patient_1:
                flash("patient found", "success")
            return render_template('billing.html',patient=patient)
        flash("patient found", "success")
    return render_template('billing.html', form=form)


# ==================================================================================
#                                 Delete the user Session
# ==================================================================================


@app.route("/logout")
def logout():
    # Remove user from the session
    if 'user' in session:
        session['user'] = None
        flash("Successfully Logged Out!", "success")
    return redirect(url_for('main'))


