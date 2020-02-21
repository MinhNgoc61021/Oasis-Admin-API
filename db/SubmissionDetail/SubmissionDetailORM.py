from db import Session, Base, TableMeta
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *

from db.JudgeResult.JudgeResultORM import JudgeResult
from db.Submission.SubmissionORM import Submission
from db.Testcase.TestcaseORM import Testcase


class SubmissionDetail(Base):
    __tablename__ = 'submission_detail'

    detail_id = Column(INTEGER(11), primary_key=True)
    testcase_id = Column(ForeignKey('testcase.testcase_id'), nullable=False, index=True)
    submission_id = Column(ForeignKey('submission.submission_id'), nullable=False, index=True)
    used_memory = Column(INTEGER(11))
    used_time = Column(INTEGER(11))
    test_score = Column(INTEGER(11))
    state = Column(ForeignKey('judge_result.judge_result_id'), nullable=False, index=True)

    judge_result = relationship('JudgeResult', back_populates='submission_detail')
    submission = relationship('Submission', back_populates='submission_detail')
    testcase = relationship('Testcase', back_populates='submission_detail')


JudgeResult.submission_detail = relationship('SubmissionDetail',
                                             order_by=SubmissionDetail.state,
                                             back_populates='judge_result',
                                             cascade='all, delete, delete-orphan')

Submission.submission_detail = relationship('SubmissionDetail',
                                            order_by=SubmissionDetail.submission_id,
                                            back_populates='submission',
                                            cascade='all, delete, delete-orphan')

Testcase.submission_detail = relationship('SubmissionDetail',
                                          order_by=SubmissionDetail.testcase_id,
                                          back_populates='testcase',
                                          cascade='all, delete, delete-orphan')
