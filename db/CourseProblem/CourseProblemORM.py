from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination
from db.Course.CourseORM import Course
from db.Problem.ProblemORM import Problem


class CourseProblem(Base):
    __tablename__ = 'course_problem'
    __table_args__ = (
        Index('unique_index', 'course_id', 'problem_id', unique=True),
    )

    course_problem_id = Column(INTEGER(11), primary_key=True)
    course_id = Column(ForeignKey('course.course_id'), nullable=False, index=True)
    problem_id = Column(ForeignKey('problem.problem_id', ondelete='CASCADE'), nullable=False, index=True)
    deadline = Column(TIMESTAMP, nullable=False)

    course = relationship('Course', back_populates='course_problem')
    problem = relationship('Problem', back_populates='course_problem')


Course.course_problem = relationship('CourseProblem',
                                     order_by=CourseProblem.course_id,
                                     back_populates='course',
                                     cascade='all, delete, delete-orphan')

Problem.course_problem = relationship('CourseProblem',
                                      order_by=CourseProblem.problem_id,
                                      back_populates='problem',
                                      cascade='all, delete, delete-orphan')
