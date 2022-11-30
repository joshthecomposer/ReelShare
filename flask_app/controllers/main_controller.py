import os
from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session
from flask_app.models.file import File
from werkzeug.utils import secure_filename



@app.route('/')
def index():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    app.config['UPLOAD_FOLDER'] = f'flask_app/static/users/{session["username"]}'
    print(app.config['UPLOAD_FOLDER'])
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Please select an audio file')
            print(request.url)
            return redirect(request.url)
        if not File.allowed_file(file.filename):
            flash('File not alloweded')
            return redirect(request.url)
        if file and File.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {
                'user_id' : session['user_id'],
                'path' : f'users/{session["username"]}/{filename}'
            }
            File.save(data)
        return redirect('/dashboard')
    return render_template('upload.html')

@app.route('/files')
def view_files():
    all_files = File.get_all_files()
    return render_template('files.html', all_files=all_files)

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')