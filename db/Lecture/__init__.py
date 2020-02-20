from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination


class Lecture(Base):
    __tablename__ = 'lecture'

    lecture_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)
    course = relationship('Course', secondary='lecture_course')

    user = relationship('User', backref=backref("user_lecture", uselist=False))
