from db import Session, Base, TableMeta
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *

from db.Problem.ProblemORM import Problem


class Testcase(Base):
    __tablename__ = 'testcase'

    testcase_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    input_file = Column(String(255))
    output_file = Column(String(255))
    unit_test_file = Column(String(255))
    problem_id = Column(ForeignKey('problem.problem_id'), nullable=False, index=True)
    score = Column(INTEGER(11), server_default=text("'1'"))

    problem = relationship('Problem', back_populates='testcase')


Problem.testcase = relationship('Testcase',
                                order_by=Testcase.problem_id,
                                back_populates='problem',
                                cascade='all, delete, delete-orphan')
