from flask_app import application
from flask_app.controllers import main_controller, users, reels, files
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    application.run(debug=True)