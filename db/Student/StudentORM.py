from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination
from db.User.UserORM import User, UserSchema
from db.Admin.AdminORM import t_student_course
from db.Submission.SubmissionORM import Submission
from db.Course.CourseORM import Course


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)
    solved = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    ratio = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    dob = Column(Date)
    score = Column(INTEGER(11), server_default=text("'0'"))
    class_course = Column(String(45, 'utf8mb4_unicode_ci'))

    user = relationship('User', back_populates='student')
    courses = relationship('Course', secondary=t_student_course, lazy='dynamic')

    @classmethod
    def getRecord(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(Student).options(joinedload('user')).order_by(getattr(
                getattr(Student, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return student_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


Student.submission = relationship('Submission',
                                  order_by=Submission.student_id,
                                  back_populates='student',
                                  cascade='all, delete, delete-orphan')

User.student = relationship('Student',
                            order_by=Student.user_id,
                            back_populates='user',
                            cascade='all, delete, delete-orphan')


class StudentSchema(ModelSchema):
    user = Nested(UserSchema, only=('username', 'name', 'email', 'created_at', 'updated_at', 'actived', 'is_lock'))

    class Meta:
        model = Student


student_schema = StudentSchema(
    only=['student_id', 'code', 'dob', 'class_course', 'user'])
