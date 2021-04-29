from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..model import User




class LoginForm(FlaskForm): #child class definition
    phonenumber=IntegerField('Phonenumber: ',validators=[DataRequired()]); #create a string field
    password=PasswordField('Password: ',validators=[DataRequired()]); #create a password field
    boolean=BooleanField('remember_me'); #create a checkbox field
    submit=SubmitField('Log-in'); #create a submit field

class RegistrationForm(FlaskForm): #child class definition
    phonenumber=IntegerField('PhoneNumber: ',validators=[DataRequired()]); #integer field for phone numbers
    username=StringField('Username: ',validators=[DataRequired(),Length(1,64),Regexp('^[a-zA-z][a-zA-Z0-9_.]*$',0,'Username Must contain only numbers,charaters,dots and signs')]); #create a stringfield
    password=PasswordField('Password: ',validators=[DataRequired(),EqualTo('password2',message='Password Does not match')]); #create a password field
    password2=PasswordField('Confirm Password: ',validators=[DataRequired()]); #create a password field
    submit=SubmitField('Register'); #create a submit field

    def validate_phonenumber(self,field):
        if User.query.filter_by(phonenumber=field.data).first():
            return ValidationError('Phone number already Exists')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            return ValidationError('Username already exists')
