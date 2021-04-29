from flask import Flask,render_template,session,redirect,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField
from wtforms.validators import DataRequired


app=Flask(__name__); #create a flask object
bootstrap=Bootstrap(app); #Bootstrap app
app.config['SECRET_KEY']='This is my encryption'

class NameForm(FlaskForm): #child class name
    name=StringField('Enter Name: ',validators=[DataRequired()]) #create a stringfield
    file=FileField('Upload File: ',validators=[DataRequired()]); #create a file field
    submit=SubmitField('Submit'); #create a submit field

@app.route('/static/css/<filename>') #decorator
def css_render(filename): #function definitin
    return render_template('static/css/{}'.format(filename)); #render template

@app.route('/',methods=['GET','POST']) #decorator
def index(): #function definition
    name=None;
    form=NameForm(); #instance of a class
    if form.validate_on_submit():
        name=form.name.data; #data in stringfield
        form.name.data=''
    return render_template('index.html',form=form,name=name); #render_template

@app.route('/user',methods=['GET','POST']) #decorator
def user(): #function definition
    form=NameForm(); #instance variable
    oldname=session.get('name'); #get value of key
    if form.validate_on_submit():
        if oldname is not None and oldname!=form.name.data:
            flash('Looks like you have change your name'); #flash message
        session['name']=form.name.data
        return redirect('/user'); #redirect user
    return render_template('user.html',form=form); #render_template



if __name__=='__main__':
    app.run(debug=True);
