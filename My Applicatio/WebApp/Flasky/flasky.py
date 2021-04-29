from app import db,create_app
from app.model import Permission
from app.model import User,Role
from flask_migrate import Migrate,upgrade



app=create_app('default'); #instance of a class
migrate=Migrate(app,db);

@app.shell_context_processor #decorators
def make_shell_context(): #function definition
    return dict(db=db,User=User,Role=Role,Permission=Permission); #return dictionary

@manager.command
def deploy(): #function definition
    upgrade(); #upgrade the database
    db.create_all(); #create allthe table and database
    Role.insert_roles(); #insert roles
    Role.query.all(); #query all the database

if __name__=='__main__':
    app.run(debug=True); #run application in debug mode
