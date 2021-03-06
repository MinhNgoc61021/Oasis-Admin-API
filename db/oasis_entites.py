from db import Session, Base, TableMeta
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import *
from marshmallow_sqlalchemy.fields import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.dialects.mysql import *
from sqlalchemy_filters import apply_pagination


class Api(Base):
    __tablename__ = 'api'

    api_id = Column(INTEGER(11), primary_key=True)
    method = Column(String(10), nullable=False)
    route = Column(String(255), nullable=False)

    roles = relationship('Role', secondary='api_role')


#
# class CoreStore(Base):
#     __tablename__ = 'core_store'
#     __table_args__ = (
#         Index('SEARCH_CORE_STORE', 'key', 'value', 'type', 'environment', 'tag'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     key = Column(String(255))
#     value = Column(LONGTEXT)
#     type = Column(String(255))
#     environment = Column(String(255))
#     tag = Column(String(255))
#
#
# class FlywaySchemaHistory(Base):
#     __tablename__ = 'flyway_schema_history'
#
#     installed_rank = Column(INTEGER(11), primary_key=True)
#     version = Column(String(50))
#     description = Column(String(200), nullable=False)
#     type = Column(String(20), nullable=False)
#     script = Column(String(1000), nullable=False)
#     checksum = Column(INTEGER(11))
#     installed_by = Column(String(100), nullable=False)
#     installed_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     execution_time = Column(INTEGER(11), nullable=False)
#     success = Column(TINYINT(1), nullable=False, index=True)
#
#

#
#
#
#
#
#
# class UploadFile(Base):
#     __tablename__ = 'upload_file'
#     __table_args__ = (
#         Index('SEARCH_UPLOAD_FILE', 'name', 'hash', 'sha256', 'ext', 'mime', 'size', 'url', 'provider'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255))
#     hash = Column(String(255))
#     sha256 = Column(String(255))
#     ext = Column(String(255))
#     mime = Column(String(255))
#     size = Column(String(255))
#     url = Column(String(255))
#     provider = Column(String(255))
#     created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
#     updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#
#
# class UploadFileMorph(Base):
#     __tablename__ = 'upload_file_morph'
#     __table_args__ = (
#         Index('SEARCH_UPLOAD_FILE_MORPH', 'related_type', 'field'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     upload_file_id = Column(INTEGER(11))
#     related_id = Column(INTEGER(11))
#     related_type = Column(LONGTEXT)
#     field = Column(LONGTEXT)
#
#

class User(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER(11), primary_key=True)
    username = Column(String(16, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'))
    email = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = Column(String(255, 'utf8mb4_unicode_ci'))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    profile_pic = Column(String(45, 'utf8mb4_unicode_ci'))
    actived = Column(TINYINT(1), server_default=text("'1'"))
    is_lock = Column(TINYINT(1), server_default=text("'1'"))

    # roles = relationship('Role', secondary=t_user_role, lazy='dynamic') # consider to use True or others, more info http://flask-sqlalchemy.pocoo.org/2.3/models/

    @classmethod
    def getRecord(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(User).order_by(getattr(
                getattr(User, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return user_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getUser(cls, username):
        sess = Session()
        try:
            user = sess.query(User).filter(cls.username == username).scalar()
            return user_schema.dump(user)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def checkUser(cls, username, password):
        sess = Session()
        try:
            check = sess.query(User).filter(User.username == str(username)).scalar()
            if check is not None:
                if check_password_hash(check.password, str(password)) is True:
                    stmt = select([t_user_role]).where(t_user_role.c.user_id == check.user_id)
                    roleType = sess.execute(stmt).first()
                    if roleType[1] == 1:
                        return 'Student'
                    elif roleType[1] == 2:
                        return user_schema.dump(check), 'Lecture'
                    elif roleType[1] == 3:
                        return user_schema.dump(check), 'Admin'
                else:
                    return 'Not found'
            else:
                return 'Not found'
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchUserRecord(cls, username):
        sess = Session()
        try:
            user = sess.query(User).filter(cls.username.like('%' + username + '%')).order_by(cls.username.asc())
            return user_schema.dump(user, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, user_id, update_username, update_name, update_email, updated_at, update_actived,
                     update_is_lock, update_permission):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if sess.query(User).filter(
                    or_(cls.username == update_username, cls.email == update_email),
                    cls.user_id != user_id).scalar() is None:

                sess.query(User).filter(cls.user_id == user_id).update(
                    {cls.username: update_username,
                     cls.email: update_email,
                     cls.name: update_name,
                     cls.updated_at: updated_at,
                     cls.actived: update_actived,
                     cls.is_lock: update_is_lock})

                if update_permission == 'Sinh viên':
                    role_id = sess.query(Role.role_id).filter(Role.code == 'STUDENT').one()
                    update_student_role = t_user_role.update().where(t_user_role.c.user_id == user_id).values(
                        {'role_id': role_id})
                    sess.execute(update_student_role)

                elif update_permission == 'Giảng viên':
                    role_id = sess.query(Role.role_id).filter(Role.code == 'LECTURE').one()
                    update_lecture_role = t_user_role.update().where(t_user_role.c.user_id == user_id).values(
                        {'role_id': role_id})
                    sess.execute(update_lecture_role)

                else:
                    role_id = sess.query(Role.role_id).filter(Role.code == 'ADMIN').one()
                    new_admin_role = t_user_role.update().where(t_user_role.c.user_id == user_id).values(
                        {'role_id': role_id})
                    sess.execute(new_admin_role)

                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def createRecord(cls, username, name, email, create_at, permission, actived, is_lock, code, dob, class_course,
                     course_id):
        Role.create()
        sess = Session()
        try:
            if sess.query(User).filter(
                    or_(cls.username == username, cls.email == email)).count() < 1 and sess.query(Student).filter(
                Student.code == code).scalar() is None:
                new_user = User(username=username,
                                name=name,
                                email=email,
                                password=generate_password_hash(username).decode('utf-8'),
                                created_at=create_at,
                                profile_pic='avatar/default.png',
                                actived=actived,
                                is_lock=is_lock)
                sess.add(new_user)
                sess.commit()
                user_id = sess.query(User.user_id).filter(cls.username == username).one()
                if permission == 'Sinh viên':
                    role_id = sess.query(Role.role_id).filter(Role.code == 'STUDENT').one()
                    new_student_role = t_user_role.insert().values({'user_id': user_id[0],
                                                                    'role_id': role_id})
                    sess.execute(new_student_role)
                    if dob is not None and class_course is not None and code is not None:
                        new_student = Student(code=code,
                                              dob=dob,
                                              class_course=class_course,
                                              user_id=user_id[0])
                        sess.add(new_student)
                        sess.commit()
                        if course_id is not None:
                            student_id = sess.query(Student.student_id).filter(Student.user_id == user_id[0]).one()

                            new_student_course = t_student_course.insert().values({'student_id': student_id[0],
                                                                                   'course_id': course_id})
                            sess.execute(new_student_course)
                    else:
                        new_student = Student(code=username,
                                              user_id=user_id[0])
                        sess.add(new_student)

                elif permission == 'Giảng viên':
                    role_id = sess.query(Role.role_id).filter(Role.code == 'LECTURE').one()
                    new_lecture_role = t_user_role.insert().values({'user_id': user_id[0],
                                                                    'role_id': role_id})
                    sess.execute(new_lecture_role)
                    new_lecture = Lecture(user_id=user_id[0])
                    sess.add(new_lecture)
                else:
                    role_id = sess.query(Role.role_id).filter(Role.code == 'ADMIN').one()
                    new_admin_role = t_user_role.insert().values({'user_id': user_id[0],
                                                                  'role_id': role_id})
                    sess.execute(new_admin_role)
                    new_admin = Admin(user_id=user_id[0])
                    sess.add(new_admin)

                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecord(cls, user_id):
        sess = Session()
        try:
            delete_user_role = t_user_role.delete().where(t_user_role.c.user_id == user_id)
            sess.execute(delete_user_role)
            user = sess.query(User).filter(cls.user_id == user_id).one()
            sess.delete(user)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)

    user = relationship('User', back_populates='admin')


t_student_course = Table(
    'student_course', TableMeta,
    Column('student_id', ForeignKey('student.student_id'), primary_key=True, nullable=False),
    Column('course_id', ForeignKey('course.course_id'), primary_key=True, nullable=False, index=True)
)


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)
    solved = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    ratio = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    dob = Column(Date)
    score = Column(INTEGER(11), server_default=text("'0'"))
    class_course = Column(String(45, 'utf8mb4_unicode_ci'))

    user = relationship('User', back_populates='student')
    courses = relationship('Course', secondary=t_student_course, lazy='dynamic')

    @classmethod
    def createRecordByCourse(cls, student_id, course_id):
        sess = Session()
        try:
            new_student_course = t_student_course.insert().values({'student_id': student_id,
                                                                   'course_id': course_id})
            sess.execute(new_student_course)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecordByCourse(cls, student_id, current_course_id, update_course_id):
        sess = Session()
        try:
            new_student_course = t_student_course.update().where(t_student_course.c.course_id == current_course_id
                                                                 ).where(
                t_student_course.c.student_id == student_id).values(
                {'student_id': student_id,
                 'course_id': update_course_id})
            sess.execute(new_student_course)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getRecord(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            if sort_field.find('user.') != -1:
                sort_field = sort_field.split('user.')[1]
                query = sess.query(Student).join(User).order_by(getattr(
                    getattr(User, sort_field), sort_order)())
            else:
                query = sess.query(Student).order_by(getattr(
                    getattr(Student, sort_field), sort_order)())
                # user_query is the user object and get_record_pagination is the index data

            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return student_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getRecordByCourse(cls, course_id, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            if sort_field.find('user.') != -1:
                sort_field = sort_field.split('user.')[1]
                query = sess.query(Student).join(User).join(t_student_course).filter(
                    cls.student_id == t_student_course.c.student_id,
                    t_student_course.c.course_id == course_id).order_by(getattr(
                    getattr(User, sort_field), sort_order)())
            else:
                query = sess.query(Student).join(t_student_course).filter(
                    cls.student_id == t_student_course.c.student_id,
                    t_student_course.c.course_id == course_id).order_by(getattr(
                    getattr(Student, sort_field), sort_order)())
                # user_query is the user object and get_record_pagination is the index data

            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return student_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchStudentRecord(cls, code):
        sess = Session()
        try:
            student = sess.query(Student).filter(cls.code.like('%' + code + '%')).order_by(cls.code.asc())
            return student_schema.dump(student, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchStudentRecordFromCourse(cls, course_id, code, search_type):
        sess = Session()
        try:
            if search_type == 'in_course':
                student = sess.query(Student).join(t_student_course).filter(cls.code.like('%' + code + '%'),
                                                                            cls.student_id == t_student_course.c.student_id,
                                                                            t_student_course.c.course_id == course_id
                                                                            ).order_by(cls.code.asc())
                return student_schema.dump(student, many=True)
            else:
                student = sess.query(Student).outerjoin(t_student_course).filter(cls.code.like('%' + code + '%'),
                                                                                 t_student_course.c.student_id == None,
                                                                                 ).order_by(cls.code.asc())
                return student_schema.dump(student, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchStudentFromCourseExistence(cls, code):
        sess = Session()
        try:
            course = sess.query(Course).join(t_student_course).join(Student).filter(cls.code == code).scalar()
            student = sess.query(Student).filter(Student.code == code).scalar()
            return course_schema.dump(course), student_schema.dump(student)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, user_id, student_id, update_code, update_username, update_name, update_email, update_dob,
                     update_class_course, update_course_id, updated_at, update_actived,
                     update_is_lock):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if sess.query(User).filter(
                    or_(User.username == update_username, User.email == update_email),
                    User.user_id != user_id).scalar() is None and sess.query(Student).filter(
                Student.code == update_code, Student.user_id != user_id).scalar() is None:

                sess.query(User).filter(User.user_id == user_id).update(
                    {User.username: update_username,
                     User.email: update_email,
                     User.name: update_name,
                     User.updated_at: updated_at,
                     User.actived: update_actived,
                     User.is_lock: update_is_lock})

                sess.query(Student).filter(Student.user_id == user_id).update(
                    {Student.code: update_code,
                     Student.updated_at: updated_at,
                     Student.dob: update_dob,
                     Student.class_course: update_class_course})

                stmt = select([t_student_course]).where(t_student_course.c.student_id == student_id)
                course = sess.execute(stmt).first()
                if course is None:
                    new_student_course = t_student_course.insert().values(
                        {'student_id': student_id,
                         'course_id': update_course_id})
                    sess.execute(new_student_course)
                else:
                    update_student_course = t_student_course.update().where(
                        t_student_course.c.student_id == student_id).values(
                        {'course_id': update_course_id})
                    sess.execute(update_student_course)

                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecord(cls, user_id):
        sess = Session()
        try:
            student = sess.query(Student).filter(cls.user_id == user_id).one()
            sess.delete(student)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecordByCourse(cls, student_id, course_id):
        sess = Session()
        try:
            delete_student_course = t_student_course.delete().where(t_student_course.c.student_id == student_id).where(
                t_student_course.c.course_id == course_id)
            sess.execute(delete_student_course)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(45), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    semester_id = Column(ForeignKey('semester.semester_id'), nullable=False, index=True)

    semester = relationship('Semester', back_populates='course')
    lectures = relationship('Lecture', secondary='lecture_course')
    students = relationship('Student', secondary=t_student_course)

    @classmethod
    def getRecord(cls, semester_id, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(Course).filter(Course.semester_id == semester_id).order_by(getattr(
                getattr(Course, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return course_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def createRecord(cls, code, name, description, semester_id):
        sess = Session()
        try:
            if sess.query(Course).filter(cls.code == code, cls.semester_id == semester_id).scalar() is None:
                new_course = Course(code=code,
                                    name=name,
                                    description=description,
                                    semester_id=semester_id)
                sess.add(new_course)
                sess.commit()

                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, course_id, update_code, update_name, update_description, update_at, semester_id):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if semester_id == '':
                sess.query(Course).filter(cls.course_id == course_id).update(
                    {cls.name: update_name,
                     cls.code: update_code,
                     cls.description: update_description,
                     cls.updated_at: update_at})
                sess.commit()
            else:
                sess.query(Course).filter(cls.course_id == course_id).update(
                    {cls.name: update_name,
                     cls.code: update_code,
                     cls.description: update_description,
                     cls.updated_at: update_at,
                     cls.semester_id: semester_id})
                sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchCourseRecord(cls, code):
        sess = Session()
        try:
            course = sess.query(Course).filter(cls.code.like('%' + code + '%')).order_by(cls.code.asc())
            return course_schema.dump(course, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchCourseExistence(cls, code):
        sess = Session()
        try:
            course = sess.query(Course).filter(cls.code == code).scalar()
            return course_schema.dump(course)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getStudentCourse(cls, student_id):
        sess = Session()
        try:
            stmt = select([t_student_course]).where(t_student_course.c.student_id == student_id)
            course_id = sess.execute(stmt).first()
            if course_id is None:
                return None
            else:
                course = sess.query(Course).filter(cls.course_id == int(course_id[1])).one()
                return course_schema.dump(course)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getAllRecord(cls):
        sess = Session()
        try:
            course = sess.query(Course).all()
            return course_schema.dump(course, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecord(cls, course_id):
        sess = Session()
        try:
            course = sess.query(Course).filter(cls.course_id == course_id).one()
            sess.delete(course)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


t_lecture_course = Table(
    'lecture_course', TableMeta,
    Column('lecture_id', ForeignKey('lecture.lecture_id'), primary_key=True, nullable=False),
    Column('course_id', ForeignKey('course.course_id'), primary_key=True, nullable=False, index=True)
)


class Submission(Base):
    __tablename__ = 'submission'

    submission_id = Column(INTEGER(11), primary_key=True)
    student_id = Column(ForeignKey('student.student_id'), nullable=False, index=True)
    course_problem_id = Column(ForeignKey('course_problem.course_problem_id'), nullable=False, index=True)
    sourcecode_file = Column(String(255), nullable=False)
    compilation_log = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    total_score = Column(INTEGER(11), server_default=text("'0'"))
    total_time = Column(INTEGER(11), server_default=text("'0'"))
    max_memory = Column(INTEGER(11), server_default=text("'0'"))
    runtime_result_id = Column(ForeignKey('judge_result.judge_result_id'), index=True, server_default=text("'1'"))

    course_problem = relationship('CourseProblem', back_populates='submission')
    runtime_result = relationship('JudgeResult', back_populates='submission')
    student = relationship('Student', back_populates='submission')


t_api_role = Table(
    'api_role', TableMeta,
    Column('api_id', ForeignKey('api.api_id'), nullable=False, index=True),
    Column('role_id', ForeignKey('role.role_id'), nullable=False, index=True)
)


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


class CourseProblem(Base):
    __tablename__ = 'course_problem'
    __table_args__ = (
        Index('unique_index', 'course_id', 'problem_id', unique=True),
    )

    course_problem_id = Column(INTEGER(11), primary_key=True)
    course_id = Column(ForeignKey('course.course_id'), nullable=False, index=True)
    problem_id = Column(ForeignKey('problem.problem_id', ondelete='CASCADE'), nullable=False, index=True)
    deadline = Column(TIMESTAMP, nullable=False)

    course = relationship('Course', back_populates='course_problem')
    problem = relationship('Problem', back_populates='course_problem')


class JudgeResult(Base):
    __tablename__ = 'judge_result'

    judge_result_id = Column(INTEGER(11), primary_key=True)
    judge_result_slug = Column(String(8))
    judge_result_name = Column(String(32))


class Lecture(Base):
    __tablename__ = 'lecture'

    lecture_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP)
    user_id = Column(ForeignKey('user.user_id'), nullable=False, unique=True)
    course = relationship('Course', secondary='lecture_course')

    user = relationship('User', backref=backref("user_lecture", uselist=False))

    @classmethod
    def createRecordByCourse(cls, course_id, user_id):
        sess = Session()
        try:
            if sess.query(User).join(Lecture).join(t_lecture_course).filter(
                    User.user_id == user_id,
                    cls.lecture_id == t_lecture_course.c.lecture_id,
                    t_lecture_course.c.course_id == course_id
            ).scalar() is None:

                getLecturer = sess.query(Lecture).filter(cls.user_id == user_id).one()

                new_lecturer_course = t_lecture_course.insert().values({'lecture_id': getLecturer.lecture_id,
                                                                        'course_id': course_id})
                sess.execute(new_lecturer_course)
                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getRecord(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(User).join(Lecture).order_by(getattr(
                getattr(User, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return user_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getRecordByCourse(cls, course_id, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(User).join(Lecture).join(t_lecture_course).filter(
                cls.lecture_id == t_lecture_course.c.lecture_id, t_lecture_course.c.course_id == course_id).order_by(
                getattr(
                    getattr(User, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return user_schema.dump(query, many=True), get_record_pagination
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchLecturerRecord(cls, name):
        sess = Session()
        try:
            lecturer = sess.query(User).join(Lecture).filter(User.name.like('%' + name + '%')).order_by(
                User.name.asc())

            return user_schema.dump(lecturer, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchLecturerRecordFromCourse(cls, course_id, name, search_type):
        sess = Session()
        try:
            if search_type == 'in_course':
                lecturer = sess.query(User).join(Lecture).join(t_lecture_course).filter(
                    User.username.like('%' + name + '%'),
                    cls.lecture_id == t_lecture_course.c.lecture_id,
                    t_lecture_course.c.course_id == course_id
                ).order_by(User.name.asc())

                return user_schema.dump(lecturer, many=True)
            else:
                lecturer = sess.query(User).join(Lecture).join(t_lecture_course).distinct(
                    t_lecture_course.c.lecture_id).filter(
                    User.username.like('%' + name + '%'),
                    cls.lecture_id == t_lecture_course.c.lecture_id,
                    t_lecture_course.c.course_id != course_id,
                ).order_by(User.name.asc())

                return user_schema.dump(lecturer, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, user_id, update_username, update_name, update_email, updated_at, update_actived,
                     update_is_lock):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if sess.query(User).filter(
                    or_(User.username == update_username, User.email == update_email),
                    User.user_id != user_id).scalar() is None:

                sess.query(User).filter(User.user_id == user_id).update(
                    {User.username: update_username,
                     User.email: update_email,
                     User.name: update_name,
                     User.updated_at: updated_at,
                     User.actived: update_actived,
                     User.is_lock: update_is_lock})

                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecord(cls, user_id):
        sess = Session()
        try:
            delete_lecture_role = t_user_role.delete().where(t_user_role.c.user_id == user_id)
            sess.execute(delete_lecture_role)
            lecturer = sess.query(User).filter(User.user_id == user_id).one()
            sess.delete(lecturer)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecordByCourse(cls, user_id, course_id):
        sess = Session()
        try:
            getLecturer = sess.query(Lecture).filter(cls.user_id == user_id).one()
            delete_lecturer_course = t_lecture_course.delete().where(
                t_lecture_course.c.lecture_id == getLecturer.lecture_id).where(
                t_lecture_course.c.course_id == course_id)
            sess.execute(delete_lecturer_course)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


class ProblemCategory(Base):
    __tablename__ = 'problem_category'

    category_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)


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
    junit_rate = Column(DOUBLE, nullable=False, server_default=text("'0.4'"))
    mark_io = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    mark_junit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    mark_parser = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    parser_rate = Column(DOUBLE, nullable=False, server_default=text("'0.6'"))
    submit_type = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'CODE'"))
    sample_code = Column(MEDIUMTEXT)
    category_id = Column(ForeignKey('problem_category.category_id'), nullable=False, index=True)
    # memory_limit = Column(INTEGER(11))
    # used_limit = Column(INTEGER(11))
    # sample_input = Column(Text(collation='utf8mb4_unicode_ci'))
    # sample_output = Column(Text(collation='utf8mb4_unicode_ci'))
    # explanation = Column(Text(collation='utf8mb4_unicode_ci'))

    category = relationship('ProblemCategory', back_populates='problem')

    @classmethod
    def createRecord(cls, created_at, title, problem_statement, input_format, constraints, output_format, level, point,
                     junit_rate, mark_io, mark_junit, mark_parser, parser_rate, submit_type, sample_code, category_id):
        sess = Session()
        try:
            if sess.query(Problem).filter(
                    cls.title == title
            ).scalar() is None:
                new_problem = Problem(created_at=created_at,
                                      title=title,
                                      problem_statement=problem_statement,
                                      input_format=input_format,
                                      constraints=constraints,
                                      output_format=output_format,
                                      level=level,
                                      point=point,
                                      junit_rate=junit_rate,
                                      mark_io=mark_io,
                                      mark_junit=mark_junit,
                                      mark_parser=mark_parser,
                                      parser_rate=parser_rate,
                                      submit_type=submit_type,
                                      sample_code=sample_code,
                                      category_id=category_id)
                sess.add(new_problem)
                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, problem_id, title, problem_statement, input_format, constraints, output_format, junit_rate,
                     mark_io, mark_junit, level, point, submit_type, sample_code, mark_parser, parser_rate,
                     updated_at, category_id):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if sess.query(Problem).filter(
                    cls.title == title, cls.problem_id != problem_id
            ).scalar() is None:
                sess.query(Problem).filter(cls.problem_id == problem_id).update(
                    {cls.title: title,
                     cls.problem_statement: problem_statement,
                     cls.input_format: input_format,
                     cls.constraints: constraints,
                     cls.output_format: output_format,
                     cls.junit_rate: junit_rate,
                     cls.mark_io: mark_io,
                     cls.mark_junit: mark_junit,
                     cls.level: level,
                     cls.point: point,
                     cls.submit_type: submit_type,
                     cls.sample_code: sample_code,
                     cls.mark_parser: mark_parser,
                     cls.parser_rate: parser_rate,
                     cls.updated_at: updated_at,
                     cls.category_id: category_id})
                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getRecord(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            if sort_field.find('category.') != -1:
                sort_field = sort_field.split('category.')[1]
                query = sess.query(Problem).join(ProblemCategory).order_by(getattr(
                    getattr(ProblemCategory, sort_field), sort_order)())

                # user_query is the user object and get_record_pagination is the index data
                query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                                page_size=int(per_page))
                # many=True if user_query is a collection of many results, so that record will be serialized to a list.
                return problem_schema.dump(query, many=True), get_record_pagination

            else:
                query = sess.query(Problem).options(joinedload('category')).order_by(getattr(
                    getattr(Problem, sort_field), sort_order)())

                # user_query is the user object and get_record_pagination is the index data
                query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                                page_size=int(per_page))
                # many=True if user_query is a collection of many results, so that record will be serialized to a list.
                return problem_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecord(cls, problem_id):
        sess = Session()
        try:
            problem = sess.query(Problem).filter(cls.problem_id == problem_id).one()
            sess.delete(problem)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(INTEGER(11), primary_key=True)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    @classmethod
    def create(cls):
        sess = Session()
        try:
            if sess.query(Role).filter(cls.code == 'STUDENT').scalar() is None:
                student_role = Role(code='STUDENT', name='Sinh vien')
                sess.add(student_role)
                sess.commit()
            if sess.query(Role).filter(cls.code == 'LECTURE').scalar() is None:
                lecturer_role = Role(code='LECTURE', name='Giang vien')
                sess.add(lecturer_role)
                sess.commit()
            if sess.query(Role).filter(cls.code == 'ADMIN').scalar() is None:
                admin_role = Role(code='ADMIN', name='Admin')
                sess.add(admin_role)
                sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

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


class Semester(Base):
    __tablename__ = 'semester'

    semester_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    @classmethod
    def createRecord(cls, name):
        sess = Session()
        try:
            if sess.query(Semester).filter(cls.name == name).scalar() is None:
                new_semester = Semester(name=name)
                sess.add(new_semester)
                sess.commit()

                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getRecord(cls, page_index, per_page, sort_field, sort_order):
        sess = Session()
        try:
            query = sess.query(Semester).order_by(getattr(
                getattr(Semester, sort_field), sort_order)())

            # user_query is the user object and get_record_pagination is the index data
            query, get_record_pagination = apply_pagination(query, page_number=int(page_index),
                                                            page_size=int(per_page))
            # many=True if user_query is a collection of many results, so that record will be serialized to a list.
            return semester_schema.dump(query, many=True), get_record_pagination
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def getAllRecords(cls):
        sess = Session()
        try:
            query = sess.query(Semester).all()
            return semester_schema.dump(query, many=True)

        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def searchSemesterRecord(cls, name):
        sess = Session()
        try:
            semester = sess.query(Semester).filter(cls.name.like('%' + name + '%')).order_by(cls.name.asc())
            return semester_schema.dump(semester, many=True)
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def deleteRecord(cls, semester_id):
        sess = Session()
        try:
            semester = sess.query(Semester).filter(cls.semester_id == semester_id).one()
            sess.delete(semester)
            sess.commit()
        except:
            sess.rollback()
            raise
        finally:
            sess.close()

    @classmethod
    def updateRecord(cls, semester_id, update_name, update_at):
        sess = Session()
        try:
            # A dictionary of key - values with key being the attribute to be updated, and value being the new
            # contents of attribute
            if sess.query(Semester).filter(
                    or_(cls.name == update_name),
                    cls.semester_id != semester_id).scalar() is None:

                sess.query(Semester).filter(cls.semester_id == semester_id).update(
                    {cls.name: update_name,
                     cls.updated_at: update_at})

                sess.commit()
                return True
            else:
                return False
        except:
            sess.rollback()
            raise
        finally:
            sess.close()


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


class UserFacebook(Base):
    __tablename__ = 'user_facebook'

    user_id = Column(ForeignKey('user.user_id'), primary_key=True)
    facebook_id = Column(String(30))

    user = relationship('User', back_populates='user_facebook')


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


#
#
# class UsersPermissionsPermission(Base):
#     __tablename__ = 'users-permissions_permission'
#     __table_args__ = (
#         Index('SEARCH_USERS_PERMISSIONS_PERMISSION', 'type', 'controller', 'action', 'policy'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     type = Column(String(255))
#     controller = Column(String(255))
#     action = Column(String(255))
#     enabled = Column(TINYINT(1))
#     policy = Column(String(255))
#     role = Column(INTEGER(11))
#
#
# class UsersPermissionsRole(Base):
#     __tablename__ = 'users-permissions_role'
#     __table_args__ = (
#         Index('SEARCH_USERS_PERMISSIONS_ROLE', 'name', 'description', 'type'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(255))
#     description = Column(String(255))
#     type = Column(String(255))
#
#
# class UsersPermissionsUser(Base):
#     __tablename__ = 'users-permissions_user'
#     __table_args__ = (
#         Index('SEARCH_USERS_PERMISSIONS_USER', 'username', 'resetPasswordToken'),
#     )
#
#     id = Column(INTEGER(11), primary_key=True)
#     username = Column(String(255))
#     email = Column(String(255))
#     password = Column(String(255))
#     resetPasswordToken = Column(String(255))
#     confirmed = Column(TINYINT(1))
#     blocked = Column(TINYINT(1))
#     role = Column(INTEGER(11))
#
#

#
#

#
#


#
#     def __init__(self, **kwargs):
#         self.update(**kwargs)
#
#     def update(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]
#             if property in ():
#                 setattr(self, property, value)
#
#
#
#
#
#     def __init__(self, **kwargs):
#         self.update(**kwargs)
#
#     def update(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]
#             if property in ('code', 'user_id', 'dob', 'class_course'):
#                 setattr(self, property, value)
#
#
#
#
#
#
#
#
#
#

# relationship
User.user_facebook = relationship('UserFacebook',
                                  order_by=UserFacebook.user_id,
                                  back_populates='user',
                                  cascade='all, delete, delete-orphan')

Course.course_problem = relationship('CourseProblem',
                                     order_by=CourseProblem.course_id,
                                     back_populates='course',
                                     cascade='all, delete, delete-orphan')

Problem.course_problem = relationship('CourseProblem',
                                      order_by=CourseProblem.problem_id,
                                      back_populates='problem',
                                      cascade='all, delete, delete-orphan')

User.lecture = relationship('Lecture',
                            order_by=Lecture.user_id,
                            back_populates='user',
                            cascade='all, delete, delete-orphan')

CourseProblem.submission = relationship('Submission',
                                        order_by=Submission.course_problem_id,
                                        back_populates='course_problem',
                                        cascade='all, delete, delete-orphan')

JudgeResult.submission = relationship('Submission',
                                      order_by=Submission.runtime_result_id,
                                      back_populates='runtime_result',
                                      cascade='all, delete, delete-orphan')

Student.submission = relationship('Submission',
                                  order_by=Submission.student_id,
                                  back_populates='student',
                                  cascade='all, delete, delete-orphan')

User.student = relationship('Student',
                            order_by=Student.user_id,
                            back_populates='user',
                            cascade='all, delete, delete-orphan')

User.admin = relationship('Admin',
                          order_by=Admin.user_id,
                          back_populates='user',
                          cascade='all, delete, delete-orphan')

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

Problem.testcase = relationship('Testcase',
                                order_by=Testcase.problem_id,
                                back_populates='problem',
                                cascade='all, delete, delete-orphan')

Submission.zip_submission_result = relationship('ZipSubmissionResult',
                                                order_by=ZipSubmissionResult.submission_id,
                                                back_populates='submission',
                                                cascade='all, delete, delete-orphan')

Semester.course = relationship('Course',
                               order_by=Course.semester_id,
                               back_populates='semester',
                               cascade='all, delete, delete-orphan')

ProblemCategory.problem = relationship('Problem',
                                       order_by=Problem.category_id,
                                       back_populates='category',
                                       cascade='all, delete, delete-orphan')


# marshmallow schema for each entity for JSON deserialize
class CourseSchema(ModelSchema):
    class Meta:
        model = Course


course_schema = CourseSchema(
    only=['course_id', 'code', 'name', 'description', 'semester'])


# marshmallow schema for each entity for JSON deserialize
class RoleSchema(ModelSchema):
    class Meta:
        model = Role


class UserSchema(ModelSchema):
    role = Nested(RoleSchema)

    class Meta:
        model = User


class StudentSchema(ModelSchema):
    user = Nested(UserSchema, only=('user_id', 'username', 'name', 'email', 'actived', 'is_lock'))

    class Meta:
        model = Student


class SemesterSchema(ModelSchema):
    class Meta:
        model = Semester


class ProblemCategorySchema(ModelSchema):
    class Meta:
        model = ProblemCategory


class ProblemSchema(ModelSchema):
    junit_rate = fields.String()
    parser_rate = fields.String()
    category = Nested(ProblemCategorySchema)

    class Meta:
        model = Problem


user_schema = UserSchema(
    only=['user_id', 'username', 'name', 'email', 'actived', 'is_lock'])

role_schema = RoleSchema()

student_schema = StudentSchema(
    only=['student_id', 'code', 'dob', 'class_course', 'user'])

semester_schema = SemesterSchema(
    only=['semester_id', 'name']
)

problem_schema = ProblemSchema()
