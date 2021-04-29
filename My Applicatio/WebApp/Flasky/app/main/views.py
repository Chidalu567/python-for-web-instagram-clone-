from datetime import datetime
from flask import render_template,request,session,current_app,redirect, url_for,flash
from . import main
from flask_login import login_required,current_user
from ..decorators import admin_required,permission_required
from .forms import EditProfileForm,EditProfileAdminForm,PostForm
from ..model import User,db,Role,Permission,Post
import os


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form=PostForm(); #instance of the class
    if form.validate_on_submit() and current_user.can(Permission.Write):
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post); #add post to database
        db.session.commit(); #save changes
        return redirect(url_for('.index'));
    posts=Post.query.order_by(Post.timestamp.desc()).all()
    page=request.args.get('page',1,type=int); #page of site
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POST_PER_PAGE'],error_out=False); #create a pagination obbject
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination)

@main.route('/admin')
@login_required
@admin_required
def for_admin_only():#function definition
    return render_template('403.html');

@main.route('/moderate') #decorator
@login_required
@permission_required
def for_moderators_only(): #function definition
    return render_template('403.html');

@main.route('/user/<username>') #decorator
def user(username): #function definition
    user=User.query.filter_by(username=username).first_or_404();
    posts=user.posts.order_by(Post.timestamp.desc()).all(); #allt the post made by the user
    return render_template('user.html',user=user,posts=posts); #Render template

@main.route('/edit-profile',methods=['GET','POST']) #decorators
@login_required
def edit_profile(): #function definition
    form=EditProfileForm(); #create a class instance object
    if form.validate_on_submit():
        current_user.name=form.name.data;
        current_user.location=form.location.data;
        current_user.about_me=form.about_me.data;
        current_user.phonenumber=form.phonenumber.data;
        db.session.add(current_user._get_current_object())
        db.session.commit(); #save changes
        flash('Your Profile has been edited'); #create a flash message
        return redirect(url_for('.user',username=current_user.username)); #redirect the page
    form.phonenumber.data=current_user.phonenumber;
    form.name.data=current_user.name;
    form.location.data=current_user.location;
    form.about_me.data=current_user.about_me;
    return render_template('edit_profile.html',form=form); #render template

@main.route('/edit_profile/<int:id>',methods=['GET','POST']) #decorator
@login_required
@permission_required(Permission.Admin)
def edit_profile_admin(id): #Function definition
    user=User.query.get_or_404(id); #get object with the id or 404 error
    form=EditProfileAdminForm(user=user); #create an instance of the class

    if form.validate_on_submit():
        user.phonenumber=form.phonenumber.data
        user.username=form.username.data
        user.role=Role.query.get(form.role.data); #get the value of the database
        user.location=form.location.data
        user.name=form.name.data
        user.about_me=form.about_me.data
        db.session.add(user); #add the user to database
        db.session.commit()#save changes to database
        flash('The profile has been edited'); #create a flash message
        return redirect(url_for('.user',username=user.username));
    form.phonenumber.data=user.phonenumber
    form.username.data=user.username
    form.role.data=user.role_id
    form.location.data=user.location
    form.name.data=user.name
    form.about_me.data=user.about_me
    return render_template('edit_profile.html',form=form,user=user); #render template


@main.route('/post/<int:id>') #decorator for dynamic routing
def post(id): #function definition
    post=Post.query.get_or_404(id); #get object in database or error 404
    return render_template('post.html',posts=[post]); #render template
