import os
import secrets
import math
from PIL import Image
from flask import request, flash, url_for, current_app, redirect
from videosurfing import create_app, db, bcrypt
import time
from datetime import datetime
import subprocess
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg','jpeg','mkv','mp4','avi','wmv','webm','3gp','flv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def folder_path(title):
    fp = os.path.join(current_app.root_path, 'static','media', title)
    try:
        os.makedirs(fp)
    except:
        pass
    return fp

def convert_time(time):
    sec = int(time)
    hrs_flot = sec/3600
    min_flot = 60 * (hrs_flot - int(hrs_flot))
    sec_flot = 60 * (min_flot - int(min_flot))    
    m_sec = 1000 * (sec_flot - int(sec_flot))

    if round(m_sec) == 1000:
        sec_flot += 1
        m_sec = 0
    
    if hrs_flot < 10:
        print_hour = '0'+ str(int(hrs_flot))
    else:
        print_hour = str(int(hrs_flot))

    if min_flot < 10:
        print_minute = '0'+ str(int(min_flot))
    else:
        print_minute = str(int(min_flot))

    if sec_flot < 10:
        print_sec = '0'+ str(int(sec_flot))
    else :
        print_sec = str(int(sec_flot))

    if m_sec < 10 :
        print_msec = '00'+ str(int(m_sec))
    elif m_sec < 100 :
        print_msec = '0'+ str(int(m_sec))
    else:
        print_msec = str(int(m_sec))

    target_print_time = print_hour +':'+ print_minute +':'+ print_sec+':'+print_msec
    return target_print_time

def save_thumb_file(title, thum_file):
    picture_fn = ''
    fp = folder_path(title)
    fn = thum_file.filename
    if (thum_file.filename):
        if allowed_file(fn):
            filename = secure_filename(thum_file.filename)
            _, f_ext = os.path.splitext(filename)
            picture_fn = title + f_ext
            picture_path = os.path.join(fp, picture_fn)
            MAX_SIZE = (350, 200)
            output_size = (MAX_SIZE)
            i = Image.open(thum_file)
            i.thumbnail(output_size)
            i.save(picture_path)
    else:
        flash('File not added!','Danger')
        return redirect(url_for('vidPost.add_new'))
        
    return picture_fn
        

def save_video(title, form_thumb, vid_file, already_added):
    vid_path = ''
    fp = folder_path(title)
    if already_added:
        thumb_img = form_thumb
        vid_path = vid_file
    else:
        thumb_img = save_thumb_file(title, form_thumb)
        if allowed_file(vid_file.filename):
            filename = secure_filename(vid_file.filename)
            _, f_ext = os.path.splitext(filename)
            vid_fn = title+ f_ext
            vid_path = os.path.join(fp, vid_fn)
            vid_file.save(vid_path)
    
    return vid_path, thumb_img

def vid_duration(vid_path):
    last_saved = ''+vid_path
    
    cmd = ['ffprobe','-v', 'error', '-show_entries' ,'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', last_saved]
    duration = subprocess.check_output(cmd, shell=True)
    
    decoded_duration = duration.decode('utf-8')
    dura_min = round(float(decoded_duration) / 60, 3)
    remain_minut =  round(dura_min - int(dura_min), 3)
    seco = round(remain_minut*60)
    dura_min_save = ''
    seco_save = ''

    if dura_min < 10 :
        dura_min_save = '0'+ str(int(dura_min))
    else:
        dura_min_save = str(int(dura_min))

    if seco < 10 :
        seco_save = '0'+ str(seco)
    else:
        seco_save = str(seco)

    dura_time = dura_min_save +':'+ seco_save
     
    return decoded_duration, dura_time, last_saved


def convert(title, last_saved):
    RATIO_DICT = [
        {'ratio': '854x480','bitrate': '768k'},
        {'ratio': '640x360','bitrate': '512k'},
        {'ratio': '320x180','bitrate': '256k'}
    ]

    return_dict = [
        {
            'name_of_file':'',
            'path':'',
        },
        {
            'name_of_file':'',
            'path':'',
        },
        {
            'name_of_file':'',
            'path':'',
        }
    ]
    
    for i in range(3):
        fp = folder_path(title)
        return_dict[i]['name_of_file'] = title +'_' + RATIO_DICT[i]['ratio'][-3:] + '.mp4'
        return_dict[i]['path'] = os.path.join(fp, return_dict[i]['name_of_file'])
        out_path = os.path.join(fp, return_dict[i]['name_of_file'])

        cmd = ['ffmpeg','-y', '-i', last_saved, '-s', RATIO_DICT[i]['ratio'],'-b:v', RATIO_DICT[i]['bitrate'], '-c:a', 'aac','-b:a', '64k', out_path]
        subprocess.check_output(cmd, shell = True)
        last_saved = return_dict[i]['path']

    return return_dict



def ffmpeg_cmd(title, last_saved):
    original_vid_file = last_saved
    vid_file = last_saved
    path_name_dict = convert(title, last_saved)
    
    for i in range(3):
        #remove "path" key from dict
        del path_name_dict[i]['path']

    os.remove(vid_file)
    return path_name_dict


    '''
    path_480 = ''
    video720 = ''
    video480 = ''
    video240 = ''
    ratios = ['854x480','640x360','320x180']#'640x360',,256x144
    fp = folder_path(title)
    vid_file = last_saved

    for ratio in ratios:
        if (ratio == '854x480'):
            name_of_file = title +'_480' + '.mp4'
            out_path = os.path.join(fp, name_of_file)
            video720 = name_of_file
            cmd = ['ffmpeg','-y', '-i', last_saved, '-s', ratio,'-b:v', '768k', '-c:a', 'aac','-b:a', '64k', out_path]
            subprocess.check_output(cmd, shell = True)
            last_saved = ''+out_path 
            path_480 = last_saved

        elif (ratio =='640x360') :
            name_of_file = title +'_240' + '.mp4'
            out_path = os.path.join(fp, name_of_file)
            video480 = name_of_file
            cmd = ['ffmpeg','-y', '-i', last_saved, '-s', ratio, '-b:v', '512k', '-c:a', 'aac','-b:a', '64k',out_path]
            subprocess.check_output(cmd, shell = True)
            last_saved = ''+out_path
        
        elif (ratio == '320x180'):
            name_of_file = title +'_144' + '.mp4'
            out_path = os.path.join(fp, name_of_file)
            video240 = name_of_file
            cmd = ['ffmpeg','-y', '-i', last_saved, '-s', ratio,'-b:v', '256k', '-c:a', 'aac','-b:a', '64k', out_path]
            subprocess.check_output(cmd, shell = True)
            last_saved = ''+out_path 
        else: 
            pass
            

    os.remove(vid_file)
    return video720, video480, video240, path_480'''


def thumbnails_vtt(title, path_480, duration_float):
    # ffmpeg -y -skip_frame nokey -i file.avi -vf 'scale=128:72,tile=8x8' -an -vsync 0 keyframes%03d.png '-q:v','100'
    fp = folder_path(title)

    preview_title = title +'preview.jpg' 
    out_pre = os.path.join(fp, preview_title)
    # calculate fps ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate file.mp4

    cmd = ["ffprobe","-v", "error", "-select_streams", "v","-show_entries" ,"stream=r_frame_rate", "-of", "default=noprint_wrappers=1:nokey=1", path_480]
    out_str = subprocess.check_output(cmd, shell=True)
    
    anb = out_str.decode('utf-8').replace('\r\n','').rsplit('/',1)

    fps = round(int(anb[0])/int(anb[1]))


    th_frame = round(float(duration_float)*fps/100)

    nfps="select=not(mod(n\, "+str(th_frame) + ")),scale=630:360,tile=100x1"

    cmd = ["ffmpeg","-y","-i", path_480,"-vf",nfps,"-an", "-vsync", "0", out_pre]#'-skip_frame','nokey',
    
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell = True)
    
    while True:
        stderr= p.communicate()[1]
        print(stderr)
        stdout = p.communicate()[0].decode()
        print(stdout)

        if stdout == '' and p.poll() is not None:
            break
        if stderr:
            pass
    
    image_counter = 0
    total_frames = 0
    initmillisec = 0.0
    x_of_image = 0 
    initsecprint = '00:00:00.000'

    interval = round(th_frame*(1/fps), 3)
    
    vtt_fn = title+ '.vtt'
    vtt_path = os.path.join(fp, vtt_fn)
    
    with open(vtt_path,'w') as f:
        f.write('WEBVTT'+'\n\n')
        for i in range(0,100):
            
            file_name = title+'preview.jpg'

            target_time = initmillisec +  interval  
            target_print_time = convert_time(target_time)
            
            f.write(str(i+1)+'\n')
            f.write( initsecprint +' --> '+ target_print_time +'\n')
            f.write(''+file_name+'#xywh='+ str( x_of_image ) +','+ str(0) +','+ str(630) +','+ str(360)+'\n\n')
            x_of_image += 630
            initmillisec = target_time
            initsecprint = convert_time(initmillisec)

    f.close()
    return 
      
