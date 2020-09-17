import os

class Config:
	SECRET_KEY = '8c4368ab880c98562df0922713a5541c'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = ''
	MAIL_PASSWORD = ''
	
	
