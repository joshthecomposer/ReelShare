import os, re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aif'}
DB = 'soundflaskio_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.folder = data['folder']
        
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['username']) < 8:
            flash('Username must be at least 8 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email format')
            is_valid = False
        if data['p_confirm'] != data['password']:
            flash('Password input did not match')
            is_valid = False
        if len(data['password']) < 4:
            flash('Password must be at least 4 characters')
            is_valid = False
        if len(data['password']) >= 4:
            if not PASSWORD_REGEX.match(data['password']):
                flash('Password must contain one number, one uppercase letter, and one lowercase letter')
                is_valid = False
        return is_valid
    
    @classmethod
    def check_user_info(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s OR email = %(email)s"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def email_lookup(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def save(cls, data):
        # folder = f'flask_app/static/users/{data["username"]}'
        # os.mkdir(folder)
        query = 'INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s)'
        return connectToMySQL(DB).query_db(query, data)