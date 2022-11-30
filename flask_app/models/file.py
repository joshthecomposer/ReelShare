from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aif'}
DB = 'soundflaskio_schema'

class File:
    def __init__(self, data):
        self.id = data['id']
        self.path = data['path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO files (user_id, path) VALUES (%(user_id)s , %(path)s)"
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