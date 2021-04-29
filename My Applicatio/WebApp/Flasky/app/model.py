//codec chidalu

from . import login_manager
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime
import hashlib

class Role(db.Model): #child class definition
    __tablename__='roles'; #table name

    id=db.Column(db.Integer,primary_key=True); #create a column
    name=db.Column(db.String(64),unique=True); #create a column
    default=db.Column(db.Boolean,index=True,default=False); #create a column
    permission=db.Column(db.Integer); #create a column
    users=db.relationship('User',backref='role',lazy='dynamic'); #relationship with the User database

    def __init__(self,**kwargs): #class constructor
        super(Role,self).__init__(**kwargs);
        if self.permission is None:
            self.permission=0

    def add_permission(self,perm): #function definition
        if not self.has_permission(perm):
            self.permission+=perm;

    def remove_permission(self,perm): #function definition
        if self.has_permission(perm):
            self.permission-=perm
    def reset_permission(self): #function definition
        self.permission=0;

    def has_permission(self,perm): #function definition
        return self.permission & perm==perm;

    @staticmethod
    def insert_roles(): #function definition
        roles={'User':[Permission.Follow,Permission.Comment,Permission.Write],'Moderate':[Permission.Comment,Permission.Write,Permission.Moderate],'Administrator':[Permission.Comment,Permission.Write,Permission.Moderate,Permission.Admin,Permission.Follow]}; #python dictionary definition
        default_role='User';

        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r);
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role);
            db.session.add(role); #add role to database
        db.session.commit(); #savechanges


class User(UserMixin,db.Model): #child class definition
    __tablename__='users'; #tablename of database

    #Automatically the role column has been created here
    id=db.Column(db.Integer,primary_key=True); #create a column for id
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id')); #create a column
    username=db.Column(db.String(64),unique=True,index=True); #create a column for username
    phonenumber=db.Column(db.Integer,unique=True,index=True); #create a column for phonenumber
    password_hash=db.Column(db.String(128)); #create a column for password hash
    name=db.Column(db.String(64)); #create a column
    location=db.Column(db.String(64)); #create a column
    about_me=db.Column(db.Text()); #create a column
    member_since=db.Column(db.DateTime(),default=datetime.utcnow); #create a column
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow); #create a column

    posts=db.relationship('Post',backref='author',lazy='dynamic'); #relationship between the Post database


    @property #decorator
    def password(self): #function definition
        raise AttributeError('Password cannot be rendered as a readable Format');

    @password.setter #decorator
    def password(self,password): #function defintion
        self.password_hash=generate_password_hash(password); #generate password hash for password

    def verify_password(self,password): #function definition
        return check_password_hash(self.password_hash,password); #check password hash with password

    @login_manager.user_loader #decorator
    def load_user(user_id): #finction definition
        return User.query.get(int(user_id)); #return the user

    def __init__(self,**kwargs): #class constructor
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.phonenumber=='07014623633':
                self.role=Role.query.filter_by(name='Administrator').first();
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first();

    def can(self,perm): #function definition
        return self.role is not None and self.role.has_permission(perm);

    def is_administrator(self):
        return self.can(Permission.Admin);

    def ping(self): #class method
        self.last_seen=datetime.utcnow()
        db.session.add(self); #add object to database
        db.session.commit(); #save changes of database

    def gravatar(self,size=100,default='identicon',rating='g'):
        url='https://secure.gravatar.com/avatar';
        hash=hashlib.md5(self.username.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r{rating}'.format(url=url,hash=hash,size=size,default=default,rating=rating)

class Post(db.Model): #child class defnition
    __tablename__='posts';
    id=db.Column(db.Integer,primary_key=True); #create a column
    body=db.Column(db.Text); #create a column in database
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id=db.Column(db.Integer,db.ForeignKey('users.id')); #create a column in database



class Permission:
    Follow=1
    Write=2
    Comment=4
    Moderate=8
    Admin=16


class AnonymousUser(AnonymousUserMixin): #child class deinifion
    def can(self,perm): #function definition
        return False

    def is_administrator(self):
        return False;

login_manager.anonymous_user=AnonymousUser;
