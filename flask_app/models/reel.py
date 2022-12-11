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
        query = "SELECT MAX(_order) AS _order FROM reel_list WHERE reel_id = %(reel_id)s;"
        result = connectToMySQL(DB).query_db(query, data)[0]['_order']
        data['_order'] = result        
        if data['_order'] == None:
            data['_order'] = 10
        else: 
            data['_order'] += 10
        query = "INSERT INTO reel_list (file_id, reel_id, _order) VALUES (%(file_id)s, %(reel_id)s, %(_order)s)"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_reels(cls, data):
        query = "SELECT * FROM reels WHERE user_id = %(user_id)s"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_reel_by_id(cls, data):
        query = "SELECT reels.id FROM reels WHERE reels.id = %(reel_id)s;"
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
                    GROUP BY reels.id
                    ORDER BY reels.id DESC;"""
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
                'id' : one_reel.id
            }
            
            tracklist = file.File.get_tracklist(data)
            for t in tracklist:
                one_reel.tracks.append(t)
            one_user.reels.append(one_reel)
        
        return one_user
    
    @staticmethod
    def validate(data):
        is_valid = True
        if data['name'] == '':
            is_valid = False
        query = "SELECT * FROM reels WHERE name = %(name)s and user_id = %(user_id)s"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        if result:
            is_valid = False
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query2 = "DELETE FROM reel_list WHERE reel_id = %(id)s;"
        query = "DELETE FROM reels WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query2, data)
        connectToMySQL(DB).query_db(query, data)
        return False
    
    @classmethod
    def get_guest_view(cls, data):
        query = "SELECT * FROM reels JOIN reel_list on reels.id = reel_list.reel_id JOIN files ON files.id = reel_list.file_id WHERE reels.id = %(id)s ORDER BY reel_list._order"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        data = {
            'id' : result[0]['id'],
            'user_id' : result[0]['user_id'],
            'name' : result[0]['name'],
            'created_at' : result[0]['created_at'],
            'updated_at' : result[0]['updated_at']
        }
        one_reel = cls(data)
        print(one_reel)
        for r in result:
            data = {
                'id' : r['files.id'],
                'user_id' : r['user_id'],
                'title' : r['title'],
                'path' : r['path'],
                'order' : r['files._order'],
                'created_at' : r['files.created_at'],
                'updated_at' : r['files.updated_at']
            }
            one_file = file.File(data)
            one_reel.tracks.append(one_file)
        return one_reel