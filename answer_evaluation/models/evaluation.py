from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .meta import Base


class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True)
    username = Column(Text)
    name = Column(Text)
    password = Column(Text)
    email_id = Column(Text)
    test_no = Column(Integer, ForeignKey('test.test_id'))
    mark = Column(Integer)



class Teacher(Base):
    __tablename__ = 'teacher'
    teacher_id = Column(Integer, primary_key=True)
    tests = relationship("Test")
    username = Column(Text)
    name = Column(Text)
    password = Column(Text)
    email_id = Column(Text)
    subject = Column(Text)


class Test(Base):
    __tablename__ = 'test'
    teach_id = Column(Integer,ForeignKey('teacher.teacher_id'))
    test_id = Column(Integer, primary_key=True)
    student = relationship("Student")
    question_id = Column(Text)
    question = Column(Text)
    answer_key = Column(Text)
    test_name = Column(Text)
