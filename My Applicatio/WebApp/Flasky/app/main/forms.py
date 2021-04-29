from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,FileField
from wtforms.validators import DataRequired,Length,Regexp,ValidationError
from ..model import User,Role
from flask_pagedown.fields import PageDownField

class EditProfileForm(FlaskForm): #child class definition
    phonenumber=StringField('Phonenumber: ',validators=[DataRequired()]); #create a stringfield
    name=StringField('RealName: ',validators=[DataRequired(),Length(0,64)]); #create a stringfield
    location=StringField('Location: ',validators=[DataRequired(),Length(0,64)]); #create a string field
    about_me=TextAreaField('About_me: '); #create a text area field
    submit=SubmitField('submit'); #create a submit field

class EditProfileAdminForm(FlaskForm): #child class definition
    phonenumber=StringField('Phonenumber: ',validators=[DataRequired()]); #create a string field
    username=StringField('Username: ',validators=[DataRequired(),Regexp('^[a-zA-Z][a-zA-Z0-9]*$',0,'Must contain only charaters,numbers,signs')]); #create a stringfield
    role=SelectField('Role',coerce=int); #create a select field
    name=StringField('RealName: ',validators=[DataRequired(),Length(0,64)]); #create a stringfield
    location=StringField('Location: ',validators=[DataRequired(),Length(0,64)]); #create a string field
    about_me=TextAreaField('About_me: '); #create a text area field
    submit=SubmitField('submit'); #create a submit field

    def __init__(self,user,*args,**kwargs): #class constructor definition
        super(EditProfileForm,self).__init__(*args,**kwargs);
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()];
        self.user=user;
    def validate_phonenumber(self,field): #class method definition
        if field.data != self.user.phonenumber and User.query.filter_by(phonenumber=field.data).first():
            raise ValidationError('Phonenumber already in use'); #raise validation error
    def validate_username(self,field): #child class definition
        if field.data !=self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use'); #raise validation error

class PostForm(FlaskForm): #child class definition
    body=PageDownField("What's on your mind",validators=[DataRequired()]); #create a textarea field
    submit=SubmitField('Submit'); #create a submit field
