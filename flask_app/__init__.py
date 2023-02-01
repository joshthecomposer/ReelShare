from flask import Flask
from os import environ

application = Flask(__name__)
application.secret_key = environ.get('SECRET_KEY')