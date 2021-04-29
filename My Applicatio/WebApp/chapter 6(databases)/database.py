from flask import Flask,render_template,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_mail import Mail,Message
from threading import Thread

app=Flask(__name__); #create a flask application
basedir=os.path.abspath(os.path.dirname(__file__)); #get the absolute path of file
app.config['SECRET_KEY']='This is my secret key'; #configure secret key of application
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+r"C:\Users\chidalu craving\Desktop\My Applicatio\WebApp\chapter 6(databases)\data.sqlite"; #setthe sqlalchemy database uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False; #set track modification to false
db=SQLAlchemy(app); #create a database object
Bootstrap(app); #Bootstrap the app

app.config['MAIL_SERVER']='smtp.gmail.com'; #ipaddress of host
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME'); #username of sennder
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD'); #password of sender
app.config['MAIL_USE_TLS']=True;#enable use transport layer security security
mail=Mail(app); #create a mail object

app.config['FLASKY_MAIL_SENDER']=os.environ.get('MAIL_USERNAME');; #set flask mail sender
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[FLASKY]'; #set the subject prefix
app.config['FLASKY_ADMIN']=os.environ.get('RECIPENT'); #set the admin

def send_async_mail(app,msg): #function definition
    with app.app_context():
        mail.send(msg); #send message

def send_mail(to,subject,template,**kwargs): #function definition
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENER'],recipients=[to]); #create a message object
    msg.body=render_template(template+'.txt',**kwargs); #message body
    msg.html=render_template(template+'.html',**kwargs); #html part of message
    thr=Thread(target=send_async_mail,args=[app,msg]); #create a thread object
    thr.start(); #start thread
    return thr;

class Role(db.Model): #child class definition
    __tablename__='roles'; #table name
    id=db.Column(db.Integer,primary_key=True); #create an interger column as a prmary_key
    name=db.Column(db.String(64),unique=True); #create a string column

    users=db.relationship('User',backref='role'); #database relationship to the user class with a backreference of role in the user class

class User(db.Model): #child class definition
    __tablename__='users';#table name
    id=db.Column(db.Integer,primary_key=True); #create an integer column
    username=db.Column(db.String(64),unique=True); #create a string column
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id')); #create an integer column with a foreign key

class NameForm(FlaskForm): #child class definition
    name=StringField('Enter Name: ',validators=[DataRequired()]); #create a stringfield
    submit=SubmitField('Submit'); #create a submit field


@app.route('/',methods=['POST','GET']) #decorators
def index(): #function definition
    form=NameForm(); #create a form object
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first(); #get the name of user n the database if it exist

        if user is None:
            user=User(username=form.name.data); #create a row in table
            db.session.add(user); #add user to database
            db.session.commit(); #save changes
            session['known']=False;#known session to false

            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user); #function call
        else:
            session['known']=True; #set known session to true

        session['name']=form.name.data; #save name
        form.name.data='';
        return redirect(url_for('index')); #redirect user

    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known')); #render_template to user

@app.route('/static/css/bootstrap.css') #decorators
def css(): #function definition
    return render_template('static/css/bootstrap.css'); #render template

# if __name__=='__main__':
#     app.run(debug=True); #run application on debug mode
