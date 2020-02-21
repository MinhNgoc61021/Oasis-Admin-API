from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    @classmethod
    def getRecord(cls, user_id):
        sess = Session()
        try:
            stmt = select([t_user_role]).where(t_user_role.c.user_id == user_id)
            s = sess.execute(stmt)
            return s.first()[1]
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


t_user_role = Table(
    'user_role', TableMeta,
    Column('user_id', ForeignKey('user.user_id'), nullable=False, index=True),
    Column('role_id', ForeignKey('role.role_id'), nullable=False, index=True)
)


# marshmallow schema for each entity for JSON deserialize
class RoleSchema(ModelSchema):
    class Meta:
        model = Role


role_schema = RoleSchema()
