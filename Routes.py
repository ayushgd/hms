from hms import app
from datetime import datetime
from flask import render_template, session, url_for, request, redirect, flash, session, g
from .Forms import Login_form, Patient_create, Patient_delete, delete_result, Patient_update,issue_medicine_form
from .Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
from .Config import db

# store patient ID for querying
pid = 0
issue_med=None
quantity=[]
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
#                              Delete an existing patient
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
#                                   Issue Medicines
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
            global issue_med
            pid = int(form.patient_id.data)
            patient = Patient_details.query.filter(
                Patient_details.id == int(form.patient_id.data))
            for patient_1 in patient:
                if patient_1:
                
                    flash("patient found", "success")
                    issue_med=None
                    medicine=med_patient(patient_1)
                    if medicine!=None:
                    
                        return render_template("get_patient_details.html", title="Search patient", patient=patient,medicine=medicine.all())
                    else:
                        return render_template("get_patient_details.html",title="Search patient",patient=patient)
            flash("patient not found", "danger")
    return render_template("get_patient_details.html", title="Get Patient Details", form=form)
    

@app.route("/IssueMedicine", methods=["GET", "POST"])
def issue_medicine():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect(url_for('main'))
    global issue_med
    global pid
    form=issue_medicine_form()
    if form.validate_on_submit():
        name=form.medicine_name.data
        quantity=form.quantity.data
        med=Medicine.query.filter(Medicine.medicine_name==form.medicine_name.data).first()
        medid=med.id
        rate=med.medicine_amount
        if issue_med==None:
            issue_med={}
            issue_med[name]={'name' : name,'quantity' : quantity,'medid' : medid,'rate' : rate}
        else:
            issue_med[name]={'name' : name,'quantity' : quantity,'medid' : medid,'rate' : rate}
        flash("medicine added","success")
        return render_template("issue_medicine.html",form=form,medicine=issue_med)
    
    return render_template("issue_medicine.html",form=form,medicine=issue_med)


# ==================================================================================
#                                   Diagnostics
# ==================================================================================


@app.route("/GetPatientDetails/Diagnostics", methods=["GET", "POST"])
def patient_diagnosis():
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
                    return render_template("get_patient_diagnosis.html", title="Search patient", patient=patient, pid=pid)
            flash("patient not found", "danger")
    return render_template("get_patient_diagnosis.html", title="Get Patient Diagnostics", form=form)
    

@app.route("/Diagnostics", methods=["GET", "POST"])
def diagnostics():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect(url_for('main'))
    global pid
    pid = request.form.get('pid')
    return render_template("diagnostics.html", pid=pid, title="Conduct Diagnostics")


# ==================================================================================
#                                   Patient Billing
# ==================================================================================

@app.route('/FinalBilling', methods=["GET", "POST"])
def billing():
    # Check if user is already logged in or not
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
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
        flash("Successfully Logged Out!")
    return redirect(url_for('main'))


@app.route("/medicine_update",methods=["GET","POST"])
def update():
    if 'user' not in session or not session['user']:
        flash('Please Login first!', 'danger')
        return redirect(url_for('main'))
    global issue_med
    global pid
    for i in issue_med:
        med_name=str(issue_med[i]['name'])
        med_id=int(issue_med[i]['medid'])
        med_quant=int(issue_med[i]['quantity'])
        medicine=Medicine.query.filter(Medicine.medicine_name==med_name).first()
        current_quant=medicine.medicine_quantity
        new_quant=current_quant-med_quant
        patient=Patient_Medicine.query.filter(Patient_Medicine.patient_id==pid,Patient_Medicine.medicine_id==med_id).first()
        if patient==None:
            db.session.add(Patient_Medicine(patient_id=pid,medicine_quantity=med_quant,medicine_id=med_id))
            medicine.medicine_quantiy=new_quant
            db.session.commit()
    
            
            



        else:
            medicine.medicine_quantity=new_quant
            patient.medicine_quantity+=med_quant
            db.session.commit()
    issue_med=None
    flash("successfully updated","success")
    return redirect(url_for('get_patient'))


            





#function to retrieve patient medicines
def med_patient(patient):
    mid=patient.id
    if Patient_Medicine.query.filter(Patient_Medicine.patient_id==mid).first()==None:
        return None
    else:
        x=Patient_Medicine.query.join(Medicine,Patient_Medicine.medicine_id==Medicine.id).filter(Patient_Medicine.patient_id==mid)
        return x