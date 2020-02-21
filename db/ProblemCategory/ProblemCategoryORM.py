from db import Session, Base, TableMeta
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *


class ProblemCategory(Base):
    __tablename__ = 'problem_category'

    category_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
