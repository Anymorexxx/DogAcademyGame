# database/db_session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.models import Base
import os

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    """Инициализация базы данных: создание файла и таблиц."""
    if not os.path.exists("database/DogAcademy.db"):
        print("База данных не найдена. Создаём новую...")
        Base.metadata.create_all(bind=engine)
    else:
        print("База данных уже существует.")

def get_session():
    """Возвращает сессию для работы с базой данных."""
    return Session()
