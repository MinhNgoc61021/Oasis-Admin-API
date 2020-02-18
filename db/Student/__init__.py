from db import Session, Base, TableMeta
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import Table


class Student:
    StudentTable = Table('user', TableMeta, autoload=True)
