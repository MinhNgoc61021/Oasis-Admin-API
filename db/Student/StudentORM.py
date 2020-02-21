from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination
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


Student.submission = relationship('Submission',
                                  order_by=Submission.student_id,
                                  back_populates='student',
                                  cascade='all, delete, delete-orphan')
