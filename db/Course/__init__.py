from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination
from db.Lecture import Lecture
from db.Semester import Semester
from db.Admin import t_student_course


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(45), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    semester_id = Column(ForeignKey('semester.semester_id'), nullable=False, index=True)

    semester = relationship('Semester')
    lectures = relationship('Lecture', secondary='lecture_course')
    students = relationship('Student', secondary=t_student_course)


t_lecture_course = Table(
    'lecture_course', TableMeta,
    Column('lecture_id', ForeignKey('lecture.lecture_id'), primary_key=True, nullable=False),
    Column('course_id', ForeignKey('course.course_id'), primary_key=True, nullable=False, index=True)
)
