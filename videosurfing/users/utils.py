import os
import secrets
from PIL import Image
from flask import request, url_for, current_app
from videosurfing import create_app, db, bcrypt, mail
import time
from flask_mail import Message


def save_any_file(form_file):
    random_hex = secrets.token_hex(8)
    file_name = form_file.filename
    _, f_ext = os.path.split(file_name)
    file_fn = random_hex + f_ext
    folder_patth = os.path.join(current_app.root_path, 'static','uploaded_file')
    try:
        os.makedirs(folder_patth)
    except:
        pass
    picture_path = os.path.join(folder_patth, file_fn)
    form_file.save(picture_path)
    return picture_path

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splittext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset REquest',
        sender = 'rahultadola@gmail.com',
        recipients = [user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('users.reset_request', token = token, _external=True)}

    If you did not make this request hen simply ignore this email and no changes will be made.'''   
    mail.send(msg)
