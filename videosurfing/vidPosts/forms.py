from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from videosurfing.models import Productions, Feturtag


def choice_query():
    return Productions.query

def get_pk(obj):
	return str(obj)


class VideoForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	vid_file = FileField('Video', validators=[FileAllowed(['mp4', '3gp','avi', 'mkv', 'wmv'])])
	thumb_image_file = FileField('Thumbnails', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
	featurtag = TextAreaField('Tags',validators=[DataRequired()] )
	production = QuerySelectField('Production',query_factory=choice_query, allow_blank=True, get_label='name',get_pk=get_pk, validators=[DataRequired()])
	submit = SubmitField('Add Video')


class TorrentForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	magnet = StringField('Magnet Link', validators=[DataRequired()])
	thumb_image_file = FileField('Thumbnails', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
	featurtag = TextAreaField('Tags',validators=[DataRequired()] )
	production = QuerySelectField('Production',query_factory=choice_query, allow_blank=True, get_label='name',get_pk=get_pk, validators=[DataRequired()])
	submit = SubmitField('Add Magnet')

class ProductionsForm(FlaskForm):
    name = StringField('Production', validators=[DataRequired()])
    
    submit = SubmitField('Add Production')

class FeaturetagsForm(FlaskForm):
    name = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Add Tag')