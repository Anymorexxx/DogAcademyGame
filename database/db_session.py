from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.models import Base
import os

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий
Session = sessionmaker(bind=engine)

# Переменная для хранения текущей сессии
current_session = None

def init_db(refresh=False):
    """
    Инициализация базы данных: создание файла и таблиц.
    Если `refresh` равно True, удаляет и пересоздаёт таблицы.
    """
    global current_session
    if not os.path.exists("database/DogAcademy.db") or refresh:
        if refresh:
            print("Обновление базы данных: удаление старых таблиц...")
            Base.metadata.drop_all(bind=engine)  # Удаляем все таблицы

        print("Создание базы данных и таблиц...")
        Base.metadata.create_all(bind=engine)  # Создаём таблицы заново
    else:
        print("База данных уже существует. Обновление не требуется.")

    # Инициализация сессии при запуске
    current_session = get_session()

def get_session():
    """Возвращает сессию для работы с базой данных."""
    return Session()

def close_sessions():
    """Закрытие всех сессий перед выходом из программы."""
    if current_session:
        print("Закрытие сессии...")
        current_session.close()
    else:
        print("Нет активной сессии для закрытия.")
