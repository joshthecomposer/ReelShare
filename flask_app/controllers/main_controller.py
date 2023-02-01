import os, uuid
from flask_app import application as app
from flask import render_template, redirect, request, flash, url_for, session
from flask_app.models.file import File
from flask_app.models import user
from flask_app.models import reel
from werkzeug.utils import secure_filename
import boto3, botocore

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('landing.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
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
            file.filename = filename
        try:
            s3.upload_fileobj(
                file,
                app.config['S3_BUCKET'],
                file.filename,
            )
            location = "{}{}".format(app.config["S3_LOCATION"], file.filename)
            print(location)
            flash('success!')
        except Exception as e:
            print("Something Happened: ", e)
            return e
        data = {
            'user_id' : session['user_id'],
            'title' : request.form['title'],
            'path' : f"{app.config['CLOUDFRONT_URL']}/{file.filename}"
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
        one_user = user.User.get_one_user(data)[0]
        return render_template('dashboard.html', all_files=all_files, all_reels=all_reels, one_user = one_user)
    one_user = all_reels
    all_reels = all_reels.reels
    return render_template('dashboard.html', all_files=all_files, all_reels=all_reels, one_user=one_user)

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect('/')