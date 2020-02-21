from db import Session, Base, TableMeta
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination
from db.ProblemCategory.ProblemCategoryORM import ProblemCategory


class Problem(Base):
    __tablename__ = 'problem'

    problem_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    title = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    problem_statement = Column(MEDIUMTEXT, nullable=False)
    input_format = Column(MEDIUMTEXT)
    constraints = Column(MEDIUMTEXT)
    output_format = Column(MEDIUMTEXT)
    level = Column(TINYINT(4), nullable=False, server_default=text("'1'"))
    point = Column(INTEGER(11), nullable=False, server_default=text("'100'"))
    junit_rate = Column(INTEGER(11), nullable=False, server_default=text("'0.4'"))
    mark_io = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    mark_junit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    mark_parser = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    parser_rate = Column(INTEGER(11), nullable=False, server_default=text("'0.6'"))
    submit_type = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'CODE'"))
    sample_code = Column(MEDIUMTEXT)
    category_id = Column(ForeignKey('problem_category.category_id'), nullable=False, index=True)
    # memory_limit = Column(INTEGER(11))
    # used_limit = Column(INTEGER(11))
    # sample_input = Column(Text(collation='utf8mb4_unicode_ci'))
    # sample_output = Column(Text(collation='utf8mb4_unicode_ci'))
    # explanation = Column(Text(collation='utf8mb4_unicode_ci'))

    category = relationship('ProblemCategory')
