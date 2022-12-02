from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    data = {
        'username': request.form['username'],
        'email' : request.form['email']
    }
    user_exists = user.User.check_user_info(data)
    if user_exists:
        flash('Email or Username already registered')
        session['form_tried'] = 'register'
        return redirect('/')
    is_valid = user.User.validate(request.form)
    if is_valid == True:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
        }

        user_id = user.User.save(data)
        session['user_id'] = user_id
        session['username'] = data['username']
        return redirect('/dashboard')
    session['form_tried'] = 'register'
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_exists = user.User.email_lookup(data)
    if not user_exists:
        flash('Email/Password invalid')
        session['form_tried'] = 'login'
        return redirect('/')
    if not bcrypt.check_password_hash(user_exists[0]['password'], request.form['password']):
        flash('Email/Password invalid')
        session['form_tried'] = 'login'
        return redirect('/')
    session['username'] = user_exists[0]['username']
    session['user_id'] = user_exists[0]['id']
    return redirect('/dashboard')

@app.route('/view/login')
def view_login():
    return render_template('view_login.html')


