from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, file

DB = 'soundflaskio_schema'

class Reel:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.tracks = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO reels (user_id, name) VALUES (%(user_id)s, %(name)s)"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def save_track_to_reel(cls, data):
        query = "INSERT INTO reel_list (file_id, reel_id) VALUES (%(file_id)s, %(reel_id)s)"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_reels(cls, data):
        query = "SELECT * FROM reels WHERE user_id = %(user_id)s"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_reel_by_name(cls, data):
        query = "SELECT reels.id FROM reels WHERE reels.name = %(name)s"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_reels_with_tracks(cls, data):
        query =  """SELECT * FROM reels 
                    JOIN users ON reels.user_id = users.id 
                    WHERE user_id = %(user_id)s;"""
        result = connectToMySQL(DB).query_db(query, data)
        if not result:
            return result
        query2 = """SELECT * FROM reels 
                    LEFT JOIN reel_list ON reels.id = reel_list.reel_id
                    LEFT JOIN files ON files.id = reel_list.file_id
                    WHERE reels.user_id = %(user_id)s
                    GROUP BY reels.id;"""
        result2 = connectToMySQL(DB).query_db(query2, data)
        
        data = {
                'id' : result[0]['users.id'],
                'username' : result[0]['username'],
                'email' : result[0]['email'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }
        
        one_user = user.User(data)
        #make a bunch of reels, and then append tracks to those reels in this function
        #append each reel to one_user
        for row in result2:
            data = {
                'id' : row['id'],
                'user_id' : row['user_id'],
                'name' : row['name'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            one_reel = cls(data)
            data = {
                'user_id' : row['user_id'],
                'title' : row['title'],
                'name' : one_reel.name
            }
            
            tracklist = file.File.get_tracklist(data)
            for t in tracklist:
                one_reel.tracks.append(t)
            one_user.reels.append(one_reel)
        
        return one_user
    
    @classmethod
    def validate(cls, data):
        is_valid = True
        query = "SELECT * FROM reel_list WHERE file_id = %()s AND reel_id = %()s"
        result = connectToMySQL(DB).query_db(query, data)
        print("Result of reel validate is:",result)
        if result != False:
            is_valid = False
        return is_valid