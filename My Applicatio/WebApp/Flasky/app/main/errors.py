from flask import render_template
from . import main

@main.app_errorhandler(404) #decorators
def page_not_found(e): #function definition
    return render_template('404.html'); #render template

@main.app_errorhandler(500) #decorators
def internal_server_error(e): #function definition
    return render_template('500.html'); #render template
