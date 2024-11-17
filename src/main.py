from tkinter import Tk
from src.ui.auth_ui import DogAcademyApp  # Изменил на правильный путь
from database.db_session import init_db

def main():
    """Основной запуск приложения."""
    # Инициализируем базу данных
    init_db()

    # Запускаем графический интерфейс
    root = Tk()
    app = DogAcademyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
