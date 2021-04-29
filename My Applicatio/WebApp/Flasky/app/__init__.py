from flask_wtf import FlaskForm
from flask_login import LoginManager
login_manager=LoginManager(); #create an instance of the class
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_pagedown import PageDown
db=SQLAlchemy(); #create an instance of object
from flask import Flask
from .main import main
from .auth import auth
from . import model,email
from config import config



bootstrap=Bootstrap(); #create an instance of object
moment=Moment(); #create an instance of the object
pagedown=PageDown(); #create an instance of a class
login_manager.login_view='auth.login'; #set the login manager login view


def create_app(config_name): #finction definition
    app=Flask(__name__); #crate an application
    app.config.from_object(config[config_name]); #configure app from object

    app.register_blueprint(main) #register blueprint
    app.register_blueprint(auth,url_prefix='/auth'); #register blueprint

    config[config_name].init_app(app); #initilize on app
    bootstrap.init_app(app); #initialize on app
    moment.init_app(app); #initialize application
    pagedown.init_app(app); #Initiliaxze in application
    db.init_app(app); #initialize on app
    login_manager.init_app(app); #initialize in application

    return app

