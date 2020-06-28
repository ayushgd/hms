from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import datetime
from wtforms.fields.html5 import DateField
from .Models import UserStore, Patient_test, Patient_Medicine, Patient_details, Diagnosis, Medicine
# class for login page form


class Login_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

# class for patient registration form

class check_length(FlaskForm):
    def __init__(self,message,min=-1,max=-1):
        self.min=min
        self.max=max
        if not message:
            self.message="input length must be between {} and {}".format(min,max)
        self.message=message
    def __call__(self,form,field):
        size=len(str(field.data))
        if Patient_details.query.filter_by(ssn_id=str(field.data)).first() not None:
            raise ValidationError("Patient with that id alresdy exists!")
        if size<self.min or size>self.max:
            raise ValidationError(self.message)



class Patient_create(FlaskForm):
    ssn_id = IntegerField('ssn id', validators=[DataRequired('please enter SSN ID in integer format'), check_length(message="id must be 9 digits long",min=9, max=9])
    patient_name = StringField('patient name', validators=[ DataRequired('please enter name')])
    patient_age = IntegerField('patient age', validators=[ DataRequired('please enter age'), check_length(min=1, max=3, message="age should be 1-3 digits long")])
    date = DateField('enter date', format="%Y-%m-%d", validators=[ DataRequired('please enter date')], default=datetime.date.today())
    Type_of_bed = SelectField('bed type', choices=[('General ward', 'General ward'), ('Semi sharing', 'Semi sharing'), ('single room', 'single room')], validators=[DataRequired('select ward type')])
    address = StringField('enter address', validators=[DataRequired('enter the address')])
    submit= SubmitField('create')

    
        
