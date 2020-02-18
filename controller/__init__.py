from flask import Flask
from flask_cors import CORS
from controller.Student.StudentManagement import student
from controller.User.UserManagement import user
from db import init_db


def create_app():
    app = Flask(__name__)
    CORS(app)
    init_db()
    app.register_blueprint(user)
    app.register_blueprint(student)
    return app
