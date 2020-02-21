from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)

    user = relationship('User', back_populates='admin')


t_api_role = Table(
    'api_role', TableMeta,
    Column('api_id', ForeignKey('api.api_id'), nullable=False, index=True),
    Column('role_id', ForeignKey('role.role_id'), nullable=False, index=True)
)

t_student_course = Table(
    'student_course', TableMeta,
    Column('student_id', ForeignKey('student.student_id'), primary_key=True, nullable=False),
    Column('course_id', ForeignKey('course.course_id'), primary_key=True, nullable=False, index=True)
)
