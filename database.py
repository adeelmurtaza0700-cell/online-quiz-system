from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine("sqlite:///quiz.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(200))
    role = Column(String(20))  # admin, teacher, student

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    subject = Column(String(50))
    duration = Column(Integer)  # minutes
    instructions = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(Text)
    question_type = Column(String(20))  # MCQ, True/False, ShortAnswer
    options = Column(JSON, nullable=True)
    correct_answer = Column(String(200))

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
