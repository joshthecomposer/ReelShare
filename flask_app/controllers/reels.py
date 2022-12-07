from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session
from flask_app.models import reel, file

@app.route('/create_reel', methods=['POST'])
def create_reel():
    data = {
        "user_id" : session['user_id'],
        "name" : request.form['name']
    }
    is_valid = reel.Reel.validate(data)
    if is_valid:
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

@app.route("/reel/view/<int:id>")
def reeL_view(id):
    data = {
        "user_id" : session['user_id']
    }
    one_user = reel.Reel.get_reels_with_tracks(data)
    for r in one_user.reels:
        if r.id == id:
            one_reel = r
    all_files = file.File.get_all_files(data)
    print("one_reel trax ==: ", one_reel.tracks)
    return render_template('reel_view.html', one_reel = one_reel, all_files = all_files)