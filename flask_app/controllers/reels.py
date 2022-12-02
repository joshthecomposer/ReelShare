from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session
from flask_app.models import reel, file

@app.route('/create_reel', methods=['POST'])
def create_reel():
    data = {
        "user_id" : session['user_id'],
        "name" : request.form['name']
    }
    reel.Reel.save(data)
    return redirect('/dashboard')

@app.route('/reel/create')
def reel_creation_page():
    return render_template('reel_creation.html')

@app.route("/save_track_to_reel", methods=['POST'])
def save_track_to_reel():
    data = {
        'user_id' : session['user_id'],
        'title' : request.form['title'],
        'name' : request.form['name']
    }
    
    file_id = file.File.get_file_by_title(data)[0]['id']
    reel_id = reel.Reel.get_reel_by_name(data)[0]['id']
    
    print(file_id)
    print(reel_id)
    
    data = {
        'file_id' : file_id,
        'reel_id' : reel_id
    }
    
    reel.Reel.save_track_to_reel(data)
    return redirect('/dashboard')