from videosurfing import db, login_manager
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

Tag_relationship_table=db.Table('tag_relationship_table',db.Column('video_id', db.Integer, db.ForeignKey('vidinfo.id'), nullable=False), db.Column('feturtag_id', db.Integer, db.ForeignKey('feturtag.id'), nullable=False), db.PrimaryKeyConstraint('video_id', 'feturtag_id'), extend_existing=True)

class Feturtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Feturtag('{self.id}','{self.name}')"

class Productions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    vids = db.relationship('Vidinfo', backref='products', lazy=True)
    
    def __repr__(self):
        return f"Productions('{self.id}','{self.name}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    vid_posted = db.relationship('Vidinfo', backref='uploaded', lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Vidinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    vid_path720 = db.Column(db.String(50), nullable=False)
    vid_path480 = db.Column(db.String(50), nullable=False)
    vid_path240 = db.Column(db.String(50), nullable=False)
    thumb_image_file = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.String(20), nullable=False,default=datetime.utcnow)
    dura_time = db.Column(db.String(10), default=1)
    views = db.Column(db.Integer, default=1)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'), nullable=False )
    tags = db.relationship('Feturtag', secondary=Tag_relationship_table, backref='tag_videos', lazy=True)

    def __repr__(self):
        return f"Vidinfo('{self.title}','{self.date_posted}','{self.uploader_id}','{self.production_id}','{self.tags}')"

class VideoMagnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    gid = db.Column(db.String(50), nullable=False)
    magnet = db.Column(db.String(200), nullable=False)
    thumb_image_file = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.String(50), nullable=False,default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, nullable=False)
    production_id = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return f"VideoMagnet('{self.title}','{self.date_posted}','{self.uploader_id}','{self.production_id}','{self.tags}')"
