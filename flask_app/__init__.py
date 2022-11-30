from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret key'
# app.add_url_rule(
#     "/flask_app/audio/uploads/<name>", endpoint="download_file", build_only=True
# )