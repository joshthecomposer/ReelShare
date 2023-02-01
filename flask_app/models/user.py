import os, re
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import reel

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aif'}
DB = 'soundflaskio_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.reels = []
        
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
    @staticmethod
    def validate_password_change(data):
        is_valid = True
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
        query = 'INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s)'
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = """SELECT 
                    users.id AS user_id, 
                    files.id AS file_id, 
                    files.path AS file_path, 
                    reels.id AS reel_id,
                    reel_list.file_id AS reel_list_id
                    FROM users 
                    LEFT JOIN files ON files.user_id = users.id 
                    LEFT JOIN reels ON reels.user_id = users.id
                    LEFT JOIN reel_list ON files.id = reel_list.file_id
                    WHERE users.id = %(user_id)s"""
        full_query = connectToMySQL(DB).query_db(query, data)
        print("DELETE QUERY STARTED RESULT IS: ",full_query)
        for row in full_query:
            query = f"""DELETE FROM reel_list WHERE file_id = {row['file_id']}"""
            result = connectToMySQL(DB).query_db(query)
            print("DELETING REEL LIST ",result)
        query = """DELETE FROM files WHERE user_id = %(user_id)s"""
        result = connectToMySQL(DB).query_db(query, data)
        print("3rd DELETE QUERY RESULT IS ", result)
        query = """DELETE FROM reels WHERE user_id = %(user_id)s"""
        result = connectToMySQL(DB).query_db(query, data)
        print("4th DELETE QUERY RESULT IS ", result)
        query = """DELETE FROM users WHERE id = %(user_id)s"""
        connectToMySQL(DB).query_db(query, data)
        print("DELETE QUERY COMPLETE")
        return
    
    @classmethod
    def get_one_user(cls, data):
        query = """SELECT id, username, email FROM users WHERE id = %(user_id)s;"""
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """UPDATE users SET email = %(email)s WHERE id = %(id)s"""
        result = connectToMySQL(DB).query_db(query, data)
        return result
    
    @classmethod
    def update_pw(cls,data):
        query = """UPDATE users SET password = %(password)s WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query, data)