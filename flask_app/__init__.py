from flask import Flask
from os import environ

application = Flask(__name__)
application.secret_key = environ.get('SECRET_KEY')
application.config["S3_SECRET_KEY"] = environ.get('S3_SECRET_KEY')
application.config["S3_BUCKET"] = environ.get('S3_BUCKET')
application.config["S3_KEY"] = environ.get('S3_KEY')
application.config["S3_SECRET"] = environ.get('S3_SECRET')
application.config["S3_LOCATION"] = environ.get('S3_LOCATION')