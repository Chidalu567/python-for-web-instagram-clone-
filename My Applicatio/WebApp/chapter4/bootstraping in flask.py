from flask import Flask,render_template
import jinja2
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime


app=Flask(__name__); #create a flask app
bootstrap=Bootstrap(app); #Bootstrap app
moment=Moment(app); #create a Moment app



@app.route('/') #decorator
def index(): #function definition
    return render_template('index.html',current_time=datetime.utcnow()); #render template
#==>Dynamic url routing
@app.route('/static/css/<filename>')
def css(filename):
    return render_template('static/css/{}'.format(filename)) #render_template

app.route('/static/js/<filename>')
def js(filename):
    return render_template('static/js/{}'.format(filename)); #render template

#==>Dynamic url routing
@app.route('/user/<name>') #decorator
def user(name):
    return render_template('user.html',username=name); #rendertemplate

#===>Error handler throuh bootstrap
@app.errorhandler(404) #decorator
def pagenotfound(e): #function definition
    return render_template('404.html'); #render template

@app.errorhandler(500) #decorator
def internalservererror(e): #function definition
    return render_template('500.html'); #render template


