from flask import Flask
from flask_cors import CORS
from controller.User.UserManagement import user
from controller.Course.CourseManagement import course
from controller.Student.StudentManagement import student
from db import init_db


def create_app():
    app = Flask(__name__)
    CORS(app)
    init_db()
    app.register_blueprint(user)
    app.register_blueprint(student)
    app.register_blueprint(course)
    return app
