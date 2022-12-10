import os, uuid
from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session
from flask_app.models.file import File
from flask_app.models import reel
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('landing.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    app.config['UPLOAD_FOLDER'] = f'flask_app/static/users/{session["username"]}'
    if request.method == 'POST':
        if request.form['title'] == '':
            flash('Please enter a title')
            return redirect(request.url)
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Please select an audio file')
            return redirect(request.url)
        if not File.allowed_file(file.filename):
            flash('File not alloweded')
            return redirect(request.url)
        if file and File.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(session['user_id']) + "_" +  str(uuid.uuid4()) + "_" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                'user_id' : session['user_id'],
                'title' : request.form['title'],
                'path' : f'users/{session["username"]}/{filename}'
            }
            File.save(data)
        return redirect('/dashboard')
    data = {
        'user_id' : session['user_id']
    }
    all_files = File.get_all_files(data)
    all_reels = reel.Reel.get_reels_with_tracks(data)
    
    if not all_reels:
        all_reels = reel.Reel.get_reels(data)
        return render_template('dashboard.html', all_files=all_files, all_reels=all_reels)
    one_user = all_reels
    all_reels = all_reels.reels
    # for r in all_reels:
    #     print(f"reel: {r.name} tracks: {r.tracks}")
    return render_template('dashboard.html', all_files=all_files, all_reels=all_reels)

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')

@app.route('/reel_view')
def reel_view():
    return render_template('reel_view.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')