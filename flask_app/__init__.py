from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = f'flask_app/static/users'
# app.add_url_rule(
#     "/flask_app/audio/uploads/<name>", endpoint="download_file", build_only=True
# )