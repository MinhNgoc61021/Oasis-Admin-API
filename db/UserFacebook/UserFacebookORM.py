from db import Session, Base, TableMeta
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *


class UserFacebook(Base):
    __tablename__ = 'user_facebook'

    user_id = Column(ForeignKey('user.user_id'), primary_key=True)
    facebook_id = Column(String(30))

    user = relationship('User', back_populates='user_facebook')
