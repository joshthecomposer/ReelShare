from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session, jsonify
from flask_app.models import reel, file

@app.route('/create_reel', methods=['POST'])
def create_reel():
    data = {
        "user_id" : session['user_id'],
        "name" : request.form['name']
    }
    print(data)
    is_valid = reel.Reel.validate(data)
    if is_valid:
        reel.Reel.save(data)
    session['reel_creation'] = False
    return redirect('/dashboard')

@app.route("/save_track_to_reel", methods=['POST'])
def save_track_to_reel():
    
    data = {
        'user_id' : session['user_id'],
        'id' : request.form['origin_id'],
        'reel_id' : request.form['target_id']
    }
    
    file_id = file.File.get_file_by_id(data)[0]['id']
    reel_id = reel.Reel.get_reel_by_id(data)[0]['id']
    
    data = {
        'file_id' : file_id,
        'reel_id' : reel_id
    }
    
    reel.Reel.save_track_to_reel(data)
    return redirect('/dashboard')

@app.route("/reel/view/<int:id>")
def reeL_view(id):
    if 'user_id' in session:
        data = {
            "user_id" : session['user_id']
        }
        one_user = reel.Reel.get_reels_with_tracks(data)
        for r in one_user.reels:
            if r.id == id:
                one_reel = r
        session['reel_id'] = one_reel.id
    else:
        data = {
            'id' : id
        }
        list = reel.Reel.get_guest_view(data)
        one_reel = list[0]
        one_user = list[1]
        return render_template('guest_view.html', one_reel=one_reel, one_user = one_user)
    return render_template('reel_view.html', one_reel = one_reel, one_user = one_user)

@app.route('/reveal_reel_creation_box', methods=['POST'])
def reel_creation_box():
    if 'reel_creation' not in session:
        session['reel_creation'] = True
    elif session['reel_creation'] == True:
        session['reel_creation'] = False
    else: 
        session['reel_creation'] = True
    return jsonify(session['reel_creation'])

@app.route('/delete_reel', methods=['POST'])
def delete_reel():
    data = {
        'id' : request.form['reel_id']
    }
    reel.Reel.delete(data)
    return redirect('/dashboard')