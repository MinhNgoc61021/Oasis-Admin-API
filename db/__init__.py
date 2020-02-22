from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from db.Config.sqlalchemy import SQLALCHEMY_URL


# WARNING --- dialect+driver://username:password@host:port/database --- Warning, port is db, dont change it,
env = 'dev'  # prod is used for prod lOL
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
    import db.Student.StudentORM
    import db.User.UserORM
    import db.Role.RoleORM
    import db.Lecture.LectureORM
    import db.Admin.AdminORM
    import db.Course.CourseORM
    import db.Semester.SemesterORM
    import db.CourseProblem.CourseProblemORM
    import db.Problem.ProblemORM
    import db.JudgeResult.JudgeResultORM
    import db.Submission.SubmissionORM
    import db.ProblemCategory.ProblemCategoryORM
    import db.SubmissionDetail.SubmissionDetailORM
    import db.Testcase.TestcaseORM
    import db.ZipSubmissionResult.ZipSubmissionResultORM
    import db.UserFacebook.UserFacebookORM

    Base.metadata.create_all(bind=engine)
