from flask_app import app
from flask import render_template, redirect, request, flash, url_for, session, jsonify
from flask_app.models import file


@app.route('/tracklist_update', methods=['POST'])
def tracklist_update():
    if request.method == 'POST':
        getorder = request.form['order']
    getorder = getorder.split(',')
    o = 10
    for i in getorder:
        data = {
            "id" : i,
            "_order" : o,
            "reel_id" : session['reel_id']
        }
        file.File.update_order(data)
        o += 10
    return jsonify(getorder)