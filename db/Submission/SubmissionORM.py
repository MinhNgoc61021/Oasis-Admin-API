from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination
from db.JudgeResult.JudgeResultORM import JudgeResult
from db.CourseProblem.CourseProblemORM import CourseProblem


class Submission(Base):
    __tablename__ = 'submission'

    submission_id = Column(INTEGER(11), primary_key=True)
    student_id = Column(ForeignKey('student.student_id'), nullable=False, index=True)
    course_problem_id = Column(ForeignKey('course_problem.course_problem_id'), nullable=False, index=True)
    sourcecode_file = Column(String(255), nullable=False)
    compilation_log = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    total_score = Column(INTEGER(11), server_default=text("'0'"))
    total_time = Column(INTEGER(11), server_default=text("'0'"))
    max_memory = Column(INTEGER(11), server_default=text("'0'"))
    runtime_result_id = Column(ForeignKey('judge_result.judge_result_id'), index=True, server_default=text("'1'"))

    course_problem = relationship('CourseProblem', back_populates='submission')
    runtime_result = relationship('JudgeResult', back_populates='submission')
    student = relationship('Student', back_populates='submission')


CourseProblem.submission = relationship('Submission',
                                        order_by=Submission.course_problem_id,
                                        back_populates='course_problem',
                                        cascade='all, delete, delete-orphan')

JudgeResult.submission = relationship('Submission',
                                      order_by=Submission.runtime_result_id,
                                      back_populates='runtime_result',
                                      cascade='all, delete, delete-orphan')
