from flask import Blueprint
from ..model import Permission

main=Blueprint('main',__name__); #create an instance of a class(initilize the app blueprint)

from . import errors, forms, views

@main.app_context_processor
def inject_permission(): #Function definition
    return dict(Permission=Permission)
