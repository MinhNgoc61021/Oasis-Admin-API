from bcrypt import hashpw, gensalt

from db import Session, Base, TableMeta
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, MEDIUMTEXT, TINYINT
from sqlalchemy_filters import apply_pagination


# class Api(Base):
#     __tablename__ = 'api'
#
#     api_id = Column(INTEGER(11), primary_key=True)
#     method = Column(String(10), nullable=False)
#     route = Column(String(255), nullable=False)
#
#     roles = relationship('Role', secondary='api_role')
#
#
# class CoreStore(Base):
#     __tablename__ = 'core_store'
#     __table_args__ = (
#         Index('SEARCH_CORE_STORE', 'key', 'value', 'type', 'environment', 'tag'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     key = Column(String(255))
#     value = Column(LONGTEXT)
#     type = Column(String(255))
#     environment = Column(String(255))
#     tag = Column(String(255))
#
#
# class FlywaySchemaHistory(Base):
#     __tablename__ = 'flyway_schema_history'
#
#     installed_rank = Column(INTEGER(11), primary_key=True)
#     version = Column(String(50))
#     description = Column(String(200), nullable=False)
#     type = Column(String(20), nullable=False)
#     script = Column(String(1000), nullable=False)
#     checksum = Column(INTEGER(11))
#     installed_by = Column(String(100), nullable=False)
#     installed_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     execution_time = Column(INTEGER(11), nullable=False)
#     success = Column(TINYINT(1), nullable=False, index=True)
#
#
# class JudgeResult(Base):
#     __tablename__ = 'judge_result'
#
#     judge_result_id = Column(INTEGER(11), primary_key=True)
#     judge_result_slug = Column(String(8))
#     judge_result_name = Column(String(32))
#
#
# class ProblemCategory(Base):
#     __tablename__ = 'problem_category'
#
#     category_id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255), nullable=False)
#
#
class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    users = relationship('User', secondary='user_role', lazy='dynamic')


# class Semester(Base):
#     __tablename__ = 'semester'
#
#     semester_id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255), nullable=False)
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#
#
# class UploadFile(Base):
#     __tablename__ = 'upload_file'
#     __table_args__ = (
#         Index('SEARCH_UPLOAD_FILE', 'name', 'hash', 'sha256', 'ext', 'mime', 'size', 'url', 'provider'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255))
#     hash = Column(String(255))
#     sha256 = Column(String(255))
#     ext = Column(String(255))
#     mime = Column(String(255))
#     size = Column(String(255))
#     url = Column(String(255))
#     provider = Column(String(255))
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#
#
# class UploadFileMorph(Base):
#     __tablename__ = 'upload_file_morph'
#     __table_args__ = (
#         Index('SEARCH_UPLOAD_FILE_MORPH', 'related_type', 'field'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     upload_file_id = Column(INTEGER(11))
#     related_id = Column(INTEGER(11))
#     related_type = Column(LONGTEXT)
#     field = Column(LONGTEXT)
#
#
t_user_role = Table(
    'user_role', TableMeta,
    Column('user_id', ForeignKey('user.user_id'), nullable=False, index=True),
    Column('role_id', ForeignKey('role.role_id'), nullable=False, index=True)
)


class User(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER(11), primary_key=True)
    username = Column(String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'))
    email = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = Column(String(255, 'utf8mb4_unicode_ci'))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    profile_pic = Column(String(45, 'utf8mb4_unicode_ci'))
    actived = Column(TINYINT(1), server_default=text("'1'"))
    is_lock = Column(TINYINT(1), server_default=text("'1'"))

    # roles = relationship('Role', secondary=t_user_role, lazy='dynamic') # consider to use True or others, more info http://flask-sqlalchemy.pocoo.org/2.3/models/
    roles = relationship('Role', secondary=t_user_role)

    @classmethod
    def getRecords(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(User).order_by(getattr(
                getattr(User, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return user_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, uid, update_username, update_name, update_email, updated_at, update_actived, update_is_lock):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if sess.query(User).filter(
                    or_(cls.username == update_username, cls.email == update_email),
                    cls.user_id != uid).scalar() is None:

                sess.query(User).filter(user_id=uid).update(
                    {cls.username: update_username,
                     cls.email: update_email,
                     cls.name: update_name,
                     cls.updated_at: updated_at,
                     cls.actived: update_actived,
                     cls.is_lock: update_is_lock})
                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


# class UserFacebook(User):
#     __tablename__ = 'user_facebook'
#
#     user_id = Column(ForeignKey('user.user_id'), primary_key=True)
#     facebook_id = Column(String(30))
#
#
# class UsersPermissionsPermission(Base):
#     __tablename__ = 'users-permissions_permission'
#     __table_args__ = (
#         Index('SEARCH_USERS_PERMISSIONS_PERMISSION', 'type', 'controller', 'action', 'policy'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     type = Column(String(255))
#     controller = Column(String(255))
#     action = Column(String(255))
#     enabled = Column(TINYINT(1))
#     policy = Column(String(255))
#     role = Column(INTEGER(11))
#
#
# class UsersPermissionsRole(Base):
#     __tablename__ = 'users-permissions_role'
#     __table_args__ = (
#         Index('SEARCH_USERS_PERMISSIONS_ROLE', 'name', 'description', 'type'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255))
#     description = Column(String(255))
#     type = Column(String(255))
#
#
# class UsersPermissionsUser(Base):
#     __tablename__ = 'users-permissions_user'
#     __table_args__ = (
#         Index('SEARCH_USERS_PERMISSIONS_USER', 'username', 'resetPasswordToken'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     username = Column(String(255))
#     email = Column(String(255))
#     password = Column(String(255))
#     resetPasswordToken = Column(String(255))
#     confirmed = Column(TINYINT(1))
#     blocked = Column(TINYINT(1))
#     role = Column(INTEGER(11))
#
#
class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)

    user = relationship('User')


t_api_role = Table(
    'api_role', TableMeta,
    Column('api_id', ForeignKey('api.api_id'), nullable=False, index=True),
    Column('role_id', ForeignKey('role.role_id'), nullable=False, index=True)
)

t_student_course = Table(
    'student_course', TableMeta,
    Column('student_id', ForeignKey('student.student_id'), primary_key=True, nullable=False),
    Column('course_id', ForeignKey('course.course_id'), primary_key=True, nullable=False, index=True)
)


#
#
# class Course(Base):
#     __tablename__ = 'course'
#
#     course_id = Column(INTEGER(11), primary_key=True)
#     code = Column(String(45), nullable=False)
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     name = Column(String(255), nullable=False)
#     description = Column(String(255))
#     semester_id = Column(ForeignKey('semester.semester_id'), nullable=False, index=True)
#
#     semester = relationship('Semester')
#     lectures = relationship('Lecture', secondary='lecture_course')
#     students = relationship('Student', secondary=t_student_course)
#
#
# class Lecture(Base):
#     __tablename__ = 'lecture'
#
#     lecture_id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP)
#     user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)
#     course = relationship('Course', secondary='lecture_course')
#
#     user = relationship('User', backref=backref("user_lecture", uselist=False))
#
#     def __init__(self, **kwargs):
#         self.update(**kwargs)
#
#     def update(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]
#             if property in ():
#                 setattr(self, property, value)
#
#
# class Problem(Base):
#     __tablename__ = 'problem'
#
#     problem_id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     title = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
#     problem_statement = Column(MEDIUMTEXT, nullable=False)
#     input_format = Column(MEDIUMTEXT)
#     constraints = Column(MEDIUMTEXT)
#     output_format = Column(MEDIUMTEXT)
#     level = Column(TINYINT(4), nullable=False, server_default=text("'1'"))
#     point = Column(INTEGER(11), nullable=False, server_default=text("'100'"))
#     junit_rate = Column(INTEGER(11), nullable=False, server_default=text("'0.4'"))
#     mark_io = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
#     mark_junit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
#     mark_parser = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
#     parser_rate = Column(INTEGER(11), nullable=False, server_default=text("'0.6'"))
#     submit_type = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'CODE'"))
#     sample_code = Column(MEDIUMTEXT)
#     category_id = Column(ForeignKey('problem_category.category_id'), nullable=False, index=True)
#     # memory_limit = Column(INTEGER(11))
#     # used_limit = Column(INTEGER(11))
#     # sample_input = Column(Text(collation='utf8mb4_unicode_ci'))
#     # sample_output = Column(Text(collation='utf8mb4_unicode_ci'))
#     # explanation = Column(Text(collation='utf8mb4_unicode_ci'))
#
#     category = relationship('ProblemCategory')
#
#
# class Student(Base):
#     __tablename__ = 'student'
#
#     student_id = Column(INTEGER(11), primary_key=True)
#     code = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)
#     solved = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
#     ratio = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
#     dob = Column(Date)
#     score = Column(INTEGER(11), server_default=text("'0'"))
#     class_course = Column(String(45, 'utf8mb4_unicode_ci'))
#
#     user = relationship('User', backref=backref("user_student"))
#     courses = relationship('Course', secondary=t_student_course, lazy='dynamic')
#
#     def __init__(self, **kwargs):
#         self.update(**kwargs)
#
#     def update(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]
#             if property in ('code', 'user_id', 'dob', 'class_course'):
#                 setattr(self, property, value)
#
#
# class CourseProblem(Base):
#     __tablename__ = 'course_problem'
#     __table_args__ = (
#         Index('unique_index', 'course_id', 'problem_id', unique=True),
#     )
#
#     course_problem_id = Column(INTEGER(11), primary_key=True)
#     course_id = Column(ForeignKey('course.course_id'), nullable=False, index=True)
#     problem_id = Column(ForeignKey('problem.problem_id', ondelete='CASCADE'), nullable=False, index=True)
#     deadline = Column(TIMESTAMP, nullable=False)
#
#     course = relationship('Course')
#     problem = relationship('Problem')
#
#
# t_lecture_course = Table(
#     'lecture_course', TableMeta,
#     Column('lecture_id', ForeignKey('lecture.lecture_id'), primary_key=True, nullable=False),
#     Column('course_id', ForeignKey('course.course_id'), primary_key=True, nullable=False, index=True)
# )
#
#
# class Testcase(Base):
#     __tablename__ = 'testcase'
#
#     testcase_id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255), nullable=False)
#     input_file = Column(String(255))
#     output_file = Column(String(255))
#     unit_test_file = Column(String(255))
#     problem_id = Column(ForeignKey('problem.problem_id'), nullable=False, index=True)
#     score = Column(INTEGER(11), server_default=text("'1'"))
#
#     problem = relationship('Problem')
#
#
# class Submission(Base):
#     __tablename__ = 'submission'
#
#     submission_id = Column(INTEGER(11), primary_key=True)
#     student_id = Column(ForeignKey('student.student_id'), nullable=False, index=True)
#     course_problem_id = Column(ForeignKey('course_problem.course_problem_id'), nullable=False, index=True)
#     sourcecode_file = Column(String(255), nullable=False)
#     compilation_log = Column(Text)
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     total_score = Column(INTEGER(11), server_default=text("'0'"))
#     total_time = Column(INTEGER(11), server_default=text("'0'"))
#     max_memory = Column(INTEGER(11), server_default=text("'0'"))
#     runtime_result_id = Column(ForeignKey('judge_result.judge_result_id'), index=True, server_default=text("'1'"))
#
#     course_problem = relationship('CourseProblem')
#     runtime_result = relationship('JudgeResult')
#     student = relationship('Student')
#
#
# class SubmissionDetail(Base):
#     __tablename__ = 'submission_detail'
#
#     detail_id = Column(INTEGER(11), primary_key=True)
#     testcase_id = Column(ForeignKey('testcase.testcase_id'), nullable=False, index=True)
#     submission_id = Column(ForeignKey('submission.submission_id'), nullable=False, index=True)
#     used_memory = Column(INTEGER(11))
#     used_time = Column(INTEGER(11))
#     test_score = Column(INTEGER(11))
#     state = Column(ForeignKey('judge_result.judge_result_id'), nullable=False, index=True)
#
#     judge_result = relationship('JudgeResult')
#     submission = relationship('Submission')
#     testcase = relationship('Testcase')

# marshmallow for each entity for JSON deserialize
class UserSchema(ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema(
    only=['user_id', 'username', 'name', 'email', 'created_at', 'updated_at', 'actived', 'is_lock'])
