from db import Session, Base, TableMeta
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import *

from db.Submission.SubmissionORM import Submission


class ZipSubmissionResult(Base):
    __tablename__ = 'zip_submission_result'

    zip_submission_result_id = Column(INTEGER(11), primary_key=True)
    submission_id = Column(INTEGER(11), ForeignKey('submission.submission_id'), nullable=False, index=True)
    junit_score = Column(DOUBLE, server_default=text("'0'"), nullable=False)
    structure_score = Column(DOUBLE, server_default=text("'0'"), nullable=False)
    junit_errors = Column(MEDIUMTEXT)
    structure_errors = Column(MEDIUMTEXT)
    compile_errors = Column(MEDIUMTEXT)

    submission = relationship('Submission', back_populates='zip_submission_result')


Submission.zip_submission_result = relationship('ZipSubmissionResult',
                                                order_by=ZipSubmissionResult.submission_id,
                                                back_populates='submission',
                                                cascade='all, delete, delete-orphan')
