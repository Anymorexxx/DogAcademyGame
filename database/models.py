from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Auth(Base):
    __tablename__ = 'auth'
    user_id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Связь с таблицей Users
    user = relationship("Users", back_populates="auth", uselist=False)


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, ForeignKey('auth.user_id'), primary_key=True)
    dog_id = Column(Integer, ForeignKey('dogs.dog_id'))
    username = Column(String, nullable=False)
    level = Column(Integer, default=1)
    achievement = Column(Text)

    # Связи
    auth = relationship("Auth", back_populates="user")  # Обратная связь с Auth
    dog = relationship("Dogs", back_populates="users")  # Связь с таблицей Dogs
    game_sessions = relationship("GameSession", back_populates="user")  # Связь с таблицей GameSession
    notifications = relationship("Notifications", back_populates="user")  # Связь с уведомлениями


class Dogs(Base):
    __tablename__ = 'dogs'
    dog_id = Column(Integer, primary_key=True)
    breed = Column(String)
    characteristics = Column(Text)
    behavior = Column(Text)
    care_info = Column(Text)
    admin_comments = Column(Text)

    # Связь с таблицей Users
    users = relationship("Users", back_populates="dog")
    # Связь с таблицей Questions
    questions = relationship("Questions", back_populates="dog")


class Questions(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    dog_id = Column(Integer, ForeignKey('dogs.dog_id'))
    question_text = Column(Text, nullable=False)
    image_url = Column(String)
    helpful_info = Column(Text)
    incorrect_attempts = Column(Integer, default=0)

    # Связь с таблицей Dogs
    dog = relationship("Dogs", back_populates="questions")


class GameSession(Base):
    __tablename__ = 'game_sessions'
    __table_args__ = (
        UniqueConstraint('user_id', 'level', name='uix_user_level'),
    )
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    level = Column(Integer, nullable=False)
    score = Column(Integer, default=0)
    duration = Column(Integer)  # Время игры в секундах
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    health = Column(Integer, default=100)  # Здоровье
    hunger = Column(Integer, default=0)  # Голод
    sleepiness = Column(Integer, default=0)  # Сонливость

    # Связь с таблицей Users
    user = relationship("Users", back_populates="game_sessions")


class Notifications(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    is_read = Column(Boolean, default=False)  # Булевый тип для read

    # Связь с таблицей Users
    user = relationship("Users", back_populates="notifications")