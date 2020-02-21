from db import Session, Base, TableMeta
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *


class JudgeResult(Base):
    __tablename__ = 'judge_result'

    judge_result_id = Column(INTEGER(11), primary_key=True)
    judge_result_slug = Column(String(8))
    judge_result_name = Column(String(32))

