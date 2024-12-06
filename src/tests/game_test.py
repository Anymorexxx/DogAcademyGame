import tkinter as tk
from src.ui.user_ui.main_menu import UserApp
from database.db_session import create_session
from database.models import Auth, Users
import logging
from config import DATABASE_URL
from sqlalchemy import create_engine


def test_user_interface():
    """Тестовый запуск пользовательского интерфейса с обходом авторизации."""
    logging.basicConfig(level=logging.INFO)

    # Проверка пути к базе данных
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as connection:
            logging.info("Подключение к базе данных успешно.")
    except Exception as e:
        logging.error(f"Не удалось подключиться к базе данных: {e}")
        return

    # Настройка окна
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title("Dog Academy Game - Тестовый режим")

    # Данные для авторизации
    test_login = "lubluNikitu"
    test_password = "meow123"

    # Проверка авторизации или создание пользователя напрямую
    try:
        session = create_session()

        # Проверяем, существует ли пользователь в таблице Auth
        user_auth = session.query(Auth).filter_by(login=test_login, password=test_password).first()

        if not user_auth:
            logging.warning("Пользователь не найден или пароль неверный. Создаём тестового пользователя.")
            # Создаём нового пользователя в таблице Auth и Users
            new_user_auth = Auth(login=test_login, password=test_password)
            session.add(new_user_auth)
            session.commit()

            new_user = Users(username="Test User", auth=new_user_auth)
            session.add(new_user)
            session.commit()
            user_id = new_user.user_id
        else:
            # Получаем user_id пользователя из таблицы Users, связанного с Auth
            user_id = user_auth.user_id
            logging.info(f"Пользователь найден: {test_login}")

        # Запуск главного меню для пользователя
        app = UserApp(root, user_id=user_id)
        root.mainloop()

    except Exception as e:
        logging.error(f"Ошибка при взаимодействии с базой данных: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    test_user_interface()
