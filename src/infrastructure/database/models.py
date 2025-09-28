from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/spaced_repetition_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WordModel(Base):
    """SQLAlchemy model for Word"""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True)
    frequency_rank = Column(Integer)
    difficulty_level = Column(Integer, default=1)
    
    user_progress = relationship("UserProgressModel", back_populates="word")


class UserProgressModel(Base):
    """SQLAlchemy model for UserProgress"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    repetitions = Column(Integer, default=0)
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=1)  # days
    next_review = Column(DateTime)
    last_review = Column(DateTime, nullable=True)
    
    word = relationship("WordModel", back_populates="user_progress")


class StudySessionModel(Base):
    """SQLAlchemy model for StudySession"""
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    user_id = Column(String, index=True)
    correct = Column(Boolean)
    response_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    quality = Column(Integer)  # 0-5


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Creates all tables in the database"""
    Base.metadata.create_all(bind=engine)
