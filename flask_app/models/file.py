from flask import flash
import os
from flask_app.config.mysqlconnection import connectToMySQL

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aif'}
DB = 'soundflaskio_schema'

class File:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.path = data['path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """INSERT INTO files (user_id, title, path)
                    VALUES (%(user_id)s , %(title)s,  %(path)s)"""
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all_files(cls, data):
        query = "SELECT * FROM files WHERE user_id = %(user_id)s"
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
    @classmethod
    def get_file_by_id(cls, data):
        query = "SELECT files.id FROM files WHERE files.user_id = %(user_id)s AND files.id = %(id)s"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_tracklist(cls, data):
        query = """SELECT * FROM files 
                    JOIN reel_list ON files.id = reel_list.file_id 
                    JOIN reels ON reels.id = reel_list.reel_id 
                    WHERE reels.id = %(id)s 
                    ORDER BY reel_list._order;"""
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate(data):
        is_valid = True
        
        
        #TODO: Move audio file validation to here.
        return is_valid
    
    @classmethod
    def update_order(cls, data):
        query = "UPDATE reel_list SET _order = %(_order)s WHERE file_id = %(id)s AND reel_id = %(reel_id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "SELECT * FROM files WHERE id = %(id)s AND user_id = %(user_id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        _path = result[0]['path']
        query = "DELETE FROM reel_list WHERE file_id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        query = "DELETE FROM files WHERE id = %(id)s AND user_id = %(user_id)s;"

        return connectToMySQL(DB).query_db(query, data)