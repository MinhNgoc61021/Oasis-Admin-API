from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from db.config.sqlalchemy import SQLALCHEMY_URL
# create_engine connect to examrag model

# WARNING --- dialect+driver://username:password@host:port/database --- Warning, port is db, dont change it,

env = 'dev'  # prod is used for
engine = None

# MySQL
if env != 'prod':
    engine = create_engine(SQLALCHEMY_URL,
                           echo=True,
                           pool_size=5)

# echo is to set up SQLAlchemy logging

# Once base class is declared, any number of mapped classes can be defined in terms of it
# Any class below is mapped, contains the table names, columns in the database
Base = declarative_base()

TableMeta = Base.metadata

# Session class is defined using sessionmaker()
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)


def init_db():
    import db.Student, db.User, db.Role, db.Lecture, db.Admin, db.Course, db.Semester
    Base.metadata.create_all(bind=engine)
