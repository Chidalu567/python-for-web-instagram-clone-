from flask import Blueprint


auth=Blueprint('auth',__name__); #create a blueprint


from . import forms,views

