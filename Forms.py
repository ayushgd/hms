from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired,Email,Length
import datetime
from wtforms.fields.html5 import DateField

class Login_form(FlaskForm):                     #class for login page form
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    submit=SubmitField('login')

#class for patient registration form
class Patient_create(FlaskForm):
    ssn_id=IntegerField('ssn id',validators=[DataRequired('please enter age'),Length(min=9,max=9,message="id must be 9 digits long")])
    patient_name=StringField('patient name',validators=[DataRequired('please enter age')])
    patient_age=IntegerField('patient age',validators=[DataRequired('please enter age'),Length(min=1,max=3,message="age should be 1-3 digists long")])
    date=DateField('enter date', format="%Y-%m-%d",validators=[DataRequired('please enter date')],default=datetime.date.today())
    Type_of_bed=SelectField('bed type',choices=[('General ward','General ward'),('Semi sharing','Semi sharing'),('single room','single room')],validators=[DataRequired('select ward type')])
    Address=StringField('enter address',validators=[DataRequired('enter the address')])
    submit=SubmitField('create')
    
    

