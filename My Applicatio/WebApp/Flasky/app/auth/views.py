from . import auth
from .. import model
from ..model import User
from app import db
from flask import render_template,request,url_for,flash,redirect
from .forms import LoginForm,RegistrationForm
from flask_login import login_user,login_required,logout_user,current_user




@auth.route('/login',methods=['GET','POST']) #decorator
def login():
    form=LoginForm(); #create an instance of the class
    if form.validate_on_submit():
        user=User.query.filter_by(phonenumber=form.phonenumber.data).first();
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.boolean.data); #login user
            next=request.args.get('next');
            if next is None or not next.startswith('/'):
                next=url_for('main.index');
            return redirect(next);
        flash('Invalid Phonenumber or Password')
    return render_template('auth/login.html',form=form); #render template

@auth.route('/register',methods=['GET','POST']) #decorator
def register(): #function definition
    form=RegistrationForm(); #create an instance of class
    if form.validate_on_submit():
        user=User(username=form.username.data,phonenumber=form.phonenumber.data,password=form.password.data);
        db.session.add(user); #add user to database
        db.session.commit(); #save changes to database
        flash('Your Account have been created');
        return redirect(url_for('auth.login'));
    return render_template('auth/register.html',form=form); #render template

@auth.route('/logout',methods=['GET','POST']) #decorators
@login_required
def logout(): #function definition
    logout_user();
    flash('You have been logout');
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request(): #function definition
    if current_user.is_authenticated:
        current_user.ping();

