import os
import secrets
import subprocess
import sys
import traceback
import time
from datetime import datetime

import aria2p

from PIL import Image
from flask import Flask, jsonify, render_template, request, url_for,flash, redirect, abort, current_app
from videosurfing.models import User, Vidinfo, Productions, Feturtag, Tag_relationship_table, VideoMagnet
from videosurfing import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from videosurfing.vidPosts.forms import VideoForm, ProductionsForm, FeaturetagsForm, TorrentForm

from videosurfing.vidPosts.utils import save_thumb_file, save_video, vid_duration, thumbnails_vtt, ffmpeg_cmd
from flask import Blueprint
from pathlib import Path



vidPost = Blueprint('vidPost', __name__)

aria2 = aria2p.API(aria2p.Client(host="http://localhost",port=6800,secret=''))

VIDEO_EXTENSIONS = set(['mkv','mp4','avi','wmv','webm','3gp','flv'])

def allowed_vid(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in VIDEO_EXTENSIONS

def split_string(valuelist):
    data = []
    if valuelist:
        data = [x.strip() for x in valuelist.split(',')]
    return data

def add_tag(video, tag_string):
    tags = []
    tags = split_string(tag_string)
    try:
        for i in tags:
            tag = Feturtag.query.filter_by(name=i).first()
            tag.tag_videos.append(video)
            db.session.commit()
    except:
        flash('adding tag error')

@vidPost.route("/watch/<vid_id>/<title>")
def watch(vid_id,title):
    video_queried = Vidinfo.query.get_or_404(vid_id)
    folder_path = os.path.join(current_app.root_path, 'videos', title)

    tag_string = []
    
    str_date = datetime.strptime(video_queried.date_posted, '%Y-%m-%d %H:%M:%S.%f')
    formate_date = str_date.strftime('%b %d, %Y')
    
    queried_production = Productions.query.filter_by(id=video_queried.production_id).first_or_404()

    video = { 'title' : video_queried.title,
            'vid_id' : video_queried.id,
            'thumb_img' : url_for("static", filename= "media/"+video_queried.title+"/"+video_queried.thumb_image_file),
            'vid_file_720'  : url_for("static", filename= "media/"+video_queried.title+"/"+video_queried.vid_path720),
            'vid_file_480'  : url_for("static", filename= "media/"+video_queried.title+"/"+video_queried.vid_path480),
            'vid_file_240'  : url_for("static", filename= "media/"+video_queried.title+"/"+video_queried.vid_path240),
            'dura_time' : video_queried.dura_time,
            'date_posted' : formate_date,
            'views': video_queried.views,
            'production':queried_production.name,
            'uploader': video_queried.uploader_id,
            'preview_thumb': url_for("static", filename= "media/"+video_queried.title+"/"+video_queried.title+".vtt"),
            'preview_img': "/Ab ban jayegi vtt file"+"preview.jpg"
            }
    heading = 'Related'

    for tag in video_queried.tags:
        new_dict = {}
        new_dict['id']= tag.id
        new_dict['name']= tag.name
        tag_string.append(new_dict)
        
    video_queried.views += 1 
    db.session.commit()
        
    return render_template("watch.html", title=video['title'], curr_video=video, tag_string = tag_string)


@vidPost.route("/dheja_batti/productions/addnew", methods = ['GET','POST'])
@login_required
def add_new_production():
    form = ProductionsForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
               
        production = Productions(name=name)
        try:
            db.session.add(production)
            db.session.commit()
            flash('Your Production Has been Added!','success')
        except:
            flash('database problem!','success')
    
    return render_template('add_productions.html', title='Add Production', form=form, legend='Add Post')


@vidPost.route("/dheja_batti/featuretags/addnew", methods = ['GET','POST'])
@login_required
def add_new_tag():
    form = FeaturetagsForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        tag = Feturtag(name=name)
        try:
            db.session.add(tag)
            db.session.commit()
        except:
            flash('database problem!','success')
        flash('Your tag Has been Added!','success')
            
    return render_template('add_tag.html', title='Add tag', form=form, legend='Add Post')

@vidPost.route("/dheja_batti/torrent/addnew", methods = ['GET','POST'])
@login_required
def add_new_torrent():
    form = TorrentForm()
    if form.validate_on_submit():
        title = form.title.data
        thumb_image_file = form.thumb_image_file.data  
        magnet = form.magnet.data
        production = form.production.data
        production_queried = Productions.query.filter_by(name=production.name).first()
        thumb_image_path = save_thumb_file(title.strip(), thumb_image_file)
        downloadObject = aria2.add_magnet(magnet)
        if downloadObject.gid:
            
            torr_object = VideoMagnet(title=title.strip(),gid=downloadObject.gid, magnet=magnet, thumb_image_file=thumb_image_path, tags=form.featurtag.data, uploader_id=current_user.id, production_id=production_queried.id)

            try:
                db.session.add(torr_object)
                db.session.commit()

                flash('Your Magnet Has been Added!')
                return redirect(url_for('vidPost.added_torrent'))
            except:
                raise Exception('database problem!')

        else:
            flash('Adding Magnet error!')
        
    return render_template('add_magnet.html', title='Add Video', form=form, legend='Add Post')

@vidPost.route("/dheja_batti/torrents_added/processing", methods = ['GET','POST'])
@login_required
def added_torrent():
    tosend = []
    torr_queried = VideoMagnet.query.all()
    for torr in torr_queried:
        try:
            downlObj = aria2.get_download(torr.gid)
            new_dict = {}
            new_dict['add_video_link']= url_for('vidPost.add_to_video', gid=downlObj.gid)
            new_dict['title'] = torr.title
            new_dict['gid']= downlObj.gid
            new_dict['downloaded']= downlObj.status
            new_dict['magnet']= torr.magnet
            new_dict['status']=downlObj.status

        except:
            new_dict={}
            new_dict['add_video_link'] = url_for('vidPost.torr_to_video', gid=torr.gid)
            new_dict['title'] = torr.title
            new_dict['gid'] = torr.gid
            new_dict['downloaded'] = 'NotAdded'
            new_dict['magnet'] = torr.magnet
            new_dict['status'] = 'NA'
    
        tosend.append(new_dict)
    return render_template('torrents_added.html', title='Magnets', aayadeta=tosend)

#Delete torrent from our database so that it can be removed from /processing 
@vidPost.route("/dheja_batti/torrent_remove", methods = ["POST"])
@login_required
def delete_torrent():
    gid = request.form.get("gid")
    try:
        downlObjr = aria2.get_download(gid)
        aria2.remove(downlObjr, True, True, True)
    except:
        print("Can not remove from Aria2")
    torrentD = VideoMagnet.query.filter_by(gid=gid).first()
    print('Torrent Processed: '+ torrentD.title)
    if torrentD.uploader_id != current_user.id:
        abort(403)
    db.session.delete(torrentD)
    db.session.commit()
    flash('Your torrentD has been deleted!', 'success')
    return redirect(url_for('vidPost.added_torrent'))


@vidPost.route("/dheja_batti/GetMagInfo/", methods=['POST'])
@login_required
def get_mag_info():
    gid = request.form.get("gid")
    new_dict = {}
    
    try:
        downlObj = aria2.get_download(gid)
        new_dict['downloaded']= downlObj.status
        new_dict['gid']= downlObj.gid
        new_dict['completed'] = aria2.client.tell_status(gid)

    except:
        new_dict['downloaded']= 'Error'
        new_dict['gid']= gid
    tosend = []
    tosend.append(new_dict)
    return jsonify(tosend)

@vidPost.route("/dheja_batti/AddMag2Aria/", methods=['POST'])
@login_required
def add_mag_aria():
    gid = str(request.form.get("gid"))
    torr_queried = VideoMagnet.query.filter_by(gid=gid).first()
    
    
    new_dict = {}

    try:
        downlObj = aria2.get_download(gid)

        torr_queried.gid = downlObj.gid
        db.session.commit()

        new_dict['downloaded']= downlObj.status
        new_dict['gid']= downlObj.gid
    except:
        downloadObject = aria2.add_magnet(torr_queried.magnet)
        torr_queried.gid = downloadObject.gid
        db.session.commit()
        new_dict['downloaded']= downloadObject.status
        new_dict['gid']= downloadObject.gid

    tosend = []
    tosend.append(new_dict)
    return jsonify(tosend)

@vidPost.route("/dheja_batti/TorrToVideo/<string:gid>", methods = ['GET','POST'])
@login_required
def torr_to_video(gid):

    torr_queried = VideoMagnet.query.filter_by(gid=gid).first()

    try:
        downlObj = aria2.get_download(gid)
    except:
        flash("GID not Found")
        downlObj = ''
        # TODO : after removed from aria add file
        #return redirect(url_for('vidPost.added_torrent'))

    if downlObj.is_complete:
        vid_file = ''
        file_name = downlObj.name.replace('+',' ').replace('[METADATA]','')
        folder_path = os.path.join(downlObj.dir, file_name)
        
        try:
            for root, dirs, files in os.walk(downlObj.dir):
                for file in files:
                    if allowed_vid(file) :
                        print("3 ---- sabse under wali condition me")
                        vid_file = os.path.join(root, file)
        except:
            raise Exception("file not found Error")              
        
        '''
        dir_arr = os.listdir(downlObj.dir)
        for f_or_d in dir_arr:
            os.path.splitext(file)[1] == '.mp4'
            if file_name in f_or_d:
                req_ford = os.path.join(downlObj.dir, f_or_d)
                if os.path.isdir(f_or_d):
                    dir_arr = os.listdir(req_ford)'''

        thumb_already_saved = True
        
        vid_path, thumb_img = save_video(torr_queried.title, torr_queried.thumb_image_file, vid_file,  thumb_already_saved)
        duration_float, duartion, last_saved = vid_duration(vid_path)
        video720, video480, video240, path_480 = ffmpeg_cmd(torr_queried.title, last_saved)
        thumbnails_vtt(torr_queried.title, path_480, duration_float)

        video = Vidinfo(title=torr_queried.title,  vid_path240=video240, vid_path480=video480, vid_path720=video720, thumb_image_file=thumb_img, dura_time = duration, uploader_id=torr_queried.uploader_id, production_id=torr_queried.production_id)
        try:
            db.session.add(video)
            db.session.commit()            
            
        except:
            raise Exception('database problem!','success')
            return redirect(url_for('vidPost.added_torrent'))
            
        add_tag(video, torr_queried.tags)
        
        try:
            db.session.delete(torr_queried)
            db.session.commit()
        except:
            raise Exception("Error! Deleting Magnet From DATABASE and Aria2")
        flash('Your Video Has been Added!','success')
        return redirect(url_for('main.tag_page',page_name='Recent' , tag = 'recent'))
    
    else:
        flash('Download Incomplete')
        return redirect(url_for('vidPost.added_torrent'))


@vidPost.route("/dheja_batti/video/addnew", methods = ['GET','POST'])
@login_required
def add_new():
    form = VideoForm()
    thumb_already_saved = False
    path_480 = ''

    if form.validate_on_submit():
        title = form.title.data
        thumb_image_file = form.thumb_image_file.data  
        vid_file = form.vid_file.data
        production = form.production.data
        tag_string = form.featurtag.data

        production_queried = Productions.query.filter_by(name=production.name).first()
        vid_path, thumb_img = save_video(title, thumb_image_file,  vid_file, thumb_already_saved)
        duration_float, duartion, last_saved = vid_duration(vid_path)
        return_dict = ffmpeg_cmd(title, last_saved)

        thumbnails_vtt(title, return_dict[1]['name_of_file'], duration_float)

        video = Vidinfo(title=title.strip(),  vid_path240=return_dict[2]['name_of_file'], vid_path480=return_dict[1]['name_of_file'], vid_path720=return_dict[0]['name_of_file'], thumb_image_file=thumb_img, dura_time = duartion, uploader_id=current_user.id, production_id=production_queried.id)
        
        try:
            db.session.add(video)
            db.session.commit()
        except:
            flash('database problem!','success')

        add_tag(video, tag_string)
        
        flash('Your Video Has been Added!','success')
        return redirect(url_for('main.home'))
    return render_template('add_video.html', title='Add Video', form=form, legend='Add Post')



@vidPost.route("/kya_yaar/tujhe_kai_samajh/aata_ki_nahi/<int:vid_id>/update", methods = ['GET','POST'])
@login_required
def update_vid(vid_id):
    video = Vidinfo.query.get_or_404(vid_id)
    if video.uploader != current_user:
        abort(403)
    form = VideoForm()
    if form.validate_on_submit():
        video.title = form.title.data
        video.thumb_image_file = form.thumb_image_file.data
        video.vid_file= form.vid_file.data
        db.session.commit()
        flash('Your Video has been updated!','success')
        return redirect(url_for('vidPost.watch', vid_id = video.id))
    elif request.method == 'GET':
        form.title.data = video.title
        form.thumb_image_file.data = video.thumb_image_file
        form.vid_file.data = video.vid_file    
    return render_template('add_video.html', title='Update Video', form=form, legend='Update Post')



@vidPost.route("/kya_yaar/tujhe_kai_samajh/aata_ki_nahi/<int:vid_id>/delete", methods = ["POST"])
@login_required
def delete_video(vid_id):
    video = Vidinfo.query.get_or_404(vid_id)
    if video.uploader != current_user:
        abort(403)
    db.session.delete(video)
    db.session.commit()
    flash('Your video has been deleted!', 'success')
    return redirect(url_for('main.tag_page', page_name = 'recent', tag='Recent'))

@vidPost.route("/kya_yaar/tujhe_kai_samajh/aata_ki_nahi/delete", methods = ["GET"])
@login_required
def delete_video1():
    tosend = []
    new_dict={}
    vs = Vidinfo.query.order_by(Vidinfo.date_posted.desc())
    for v in vs:
        try:
            new_dict['add_video_link'] = url_for('vidPost.delete_video', vid_id=v.id)
            new_dict['title'] = v.title
            new_dict['gid'] = v.id
            new_dict['downloaded'] = v.views
        
        except:
            new_dict['add_video_link'] = ''
            new_dict['title'] = 'Unknown'
            new_dict['gid'] = 'NULL'
            new_dict['downloaded'] = '0'
    
        tosend.append(new_dict)
    return render_template('torrents_added.html', title='Delete', aayadeta=tosend)

