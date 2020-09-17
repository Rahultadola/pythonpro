import os
import secrets
from flask import Flask, jsonify, render_template, request, url_for,flash, redirect, abort, current_app
from videosurfing.models import User, Vidinfo
from videosurfing.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, UploadFileForm
from videosurfing.vidPosts.forms import VideoForm
from videosurfing import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import time
from flask_mail import Mail
from videosurfing.users.utils import send_reset_email, save_picture, save_any_file


from flask import Blueprint

users = Blueprint('users', __name__)

#this file, form, utils 127.0.0.1:5000/tane_ni_batadu_ja/hu_karleyga
@users.route("/tane_ni_batadu_ja/hu_karleyga",methods = ['GET','POST'])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        if form.file.data:
            uploaded_file = save_any_file(form.file.data)
            flash('filePath '+uploaded_file , 'success')
        else:
            flash('Select file' , '')
    return render_template("upload_file.html", title = 'UploadFile', form = form)


@users.route("/tane_ni_batadu_ja/hu_karleyga/register",methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in' , 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title = 'Register', form = form)    



@users.route("/tane_ni_batadu_ja/hu_karleyga/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title = 'Login', form = form)    


@users.route("/tane_ni_batadu_ja/hu_karleyga/logout")
def logout():
    logout_user()
    flash('You are Logged Out Successfully.', 'Normal')
    return redirect(url_for('main.home'))


@users.route("/tane_ni_batadu_ja/hu_karleyga/account", methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)



@users.route("/tane_ni_batadu_ja/hu_karleyga/reset_request", methods = ["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user :
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.','info')
            return redirect(url_for('users.login'))
        else :
            flash('No such User exist!')
    return render_template('reset_request.html', title='Reset Request', form=form, legend='Reset Password')


@users.route("/tane_ni_batadu_ja/hu_karleyga/reset_password/<token>", methods = ["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expire token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in' , 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset password', form=form, legend='Reset Password')