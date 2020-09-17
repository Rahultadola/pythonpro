import os
import secrets
from flask import Blueprint, jsonify, render_template, request, url_for, flash, redirect, abort, current_app, send_from_directory
from videosurfing.models import Vidinfo, Productions, Feturtag
from videosurfing import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import time
from flask_mail import Mail


main = Blueprint('main', __name__)

def set_heading_dict(tag_prod):
    heading_dict = {}
    try:
        heading_dict['heading_img'] = url_for('static', filename= 'production/'+tag_prod.name+'.png')
    except:
        heading_dict['heading_img'] = ''
    try:
        heading_dict['name'] = tag_prod.name.title()
    except:
        pass
    return heading_dict 

def set_data_dict(data):
    new_dict = {}
    new_dict['post_link']= url_for('vidPost.watch', title=data.title, vid_id=data.id)
    new_dict['thumb_img'] = url_for('static', filename= 'media/'+data.title+'/'+data.thumb_image_file)
    new_dict['dura_time']= data.dura_time
    new_dict['vid_name']= data.title.title()
    new_dict['views']= data.views
    
    return new_dict


@main.route("/")
@main.route("/home")
def home():
    tosend = []
    query_headings = []

    query_headings = Productions.query.all()

    for i in query_headings:
        new_dict = {}
        new_dict['name']= i.name
        tosend.append(new_dict)
    return render_template("home.html", title = 'Home', heading_name = tosend)

@main.route("/category")
def category():
    tosend = []
    query_tags = Feturtag.query.all()

    for i in query_tags:
        new_dict = {}
        new_dict['name']= i.name
        new_dict['link']= url_for('main.tag_page', page_name = 'tag', tag=i.name)
        tosend.append(new_dict)

    return render_template("category.html", title = 'Category', category_list = tosend)


@main.route("/specially/<string:page_name>/<string:tag>")
def tag_page( page_name , tag):
    
    tosend = []
    new_dict = {}
    tag_name = ''
    tuple_querd = []
    
    if 'prod' in page_name:
        tuple_querd = Productions.query.filter_by(name=tag).first_or_404()
    elif 'tag' in page_name:
        tuple_querd = Feturtag.query.filter_by(name=tag).first()
    else:
        pass

    if tuple_querd:
        new_dict['name']= tuple_querd.name
        tag_name = tuple_querd.name
    else:
        pass

    if page_name == 'recent':
        new_dict['name'] = tag
        tag_name == tag
    else:
        pass

    if page_name == 'mostviewed':
        new_dict['name'] = tag
        tag_name == tag
    else:
        pass
    
    tosend.append(new_dict)
    return render_template("for_all.html", title = tag_name.title(), tag_page_value = tosend, page_value = page_name)
    

@main.route("/yahi_chahiye", methods = ["POST"])
def yahi_chahiye():
    start = int(request.form.get("start"))
    end = int(request.form.get("end"))
    tag_string = str(request.form.get("tag_string"))
    page_name = str(request.form.get("page_value"))

    tosend = []
    data = []
    tuple_querd = []

    class ForHeading():
        '''A simple attempt to model a database tuple'''
        def __init__(self, name):
            self.name = name
    

    if page_name == 'prod':
        tuple_querd = Productions.query.filter_by(name=tag_string).first_or_404()
        if tuple_querd:
            data = tuple_querd.vids
        
    elif page_name == 'tag':
        tuple_querd = Feturtag.query.filter_by(name=tag_string).first()
        if tuple_querd:
            data = tuple_querd.tag_videos

    elif page_name == 'recent':
        data = Vidinfo.query.order_by(Vidinfo.date_posted.desc()).all()
        tuple_querd = ForHeading('Recent')

    elif page_name == 'mostviewed':
        data = Vidinfo.query.order_by(Vidinfo.views.desc()).all()
        tuple_querd = ForHeading('Top Viewed')  

    for d in data:
        print(d)   

    for i in range(start-1, end) :
        try:
            new_dict = set_data_dict(data[i])
        except:
            new_dict={}
        tosend.append(new_dict)

    heading_dict = {}
    if start < 7:
        heading_dict = set_heading_dict(tuple_querd)
        heading_dict['heading_img'] = ''

    tosend.append(heading_dict) 
    return jsonify(tosend)


@main.route("/related", methods = ["POST"])
def related():
    start = int(request.form.get("start"))
    end = int(request.form.get("end"))
    tag_string = str(request.form.get("tag_string"))

    tosend = []
    mached_data = []
    all_matched = 0
   
    while len(mached_data) <= end:
        if all_matched == len(tag_string):
            break
        else:
            for char in tag_string:
                flag = 0
                number_of_entry = 2
                tag_to_look = Feturtag.query.filter(Feturtag.id == int(char)).first_or_404()
                tag_data = tag_to_look.tag_videos
                for d in tag_data:
                    if d not in mached_data :
                        mached_data.append(d)
                        number_of_entry -= 1  
                    else:
                        flag += 1
                        
                    if number_of_entry == 0:
                        break
            if flag == len(tag_data):
                all_matched +=1
        
    for i in range(start-1, end) :
        new_dict = {}
        try:
            new_dict = set_data_dict(mached_data[i])
        except:
            pass
        
        tosend.append(new_dict)
                       
    return jsonify(tosend)


@main.route("/posts", methods = ["POST"])
def posts():
    # Get start and end point for post generate.
    start = int(request.form.get("start")  )#or 1
    end = int(request.form.get("end") )#or (start + 7)
    heading = request.form.get("heading")  
    
    data = []
    tosend = []

    query_prod = Productions.query.filter_by(name=heading).first_or_404()

    if query_prod.id:
        data = Vidinfo.query.order_by(Vidinfo.date_posted.desc()).filter(Vidinfo.production_id == query_prod.id)
        for d in data:
            print(d)

    
    for i in range(start-1, end ) :
        try:
            new_dict = set_data_dict(data[i])
        except:
            new_dict={}
        tosend.append(new_dict)

    heading_dict = set_heading_dict(tag_prod=query_prod)
    heading_dict['heading_link'] = url_for('main.tag_page', page_name = 'prod', tag = query_prod.name)
       
    tosend.append(heading_dict) 
    return jsonify(tosend)

