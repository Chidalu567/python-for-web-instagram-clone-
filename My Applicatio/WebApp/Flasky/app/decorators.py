from functools import wraps
from flask import abort
from flask_login import current_user
from .model import Permission

def permission_required(permission):
    def decorator(f): #function definition
        @wraps(f)
        def decorated_function(*args,**kwargs): #function definition
            if not current_user.can(permission):
                abort(403);
            return f(*args,**kwargs);
        return decorated_function;
    return decorator

def admin_required(f): #function definition
    return permission_required(Permission.Admin)(f);
