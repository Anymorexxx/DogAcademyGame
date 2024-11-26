import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import Tk, messagebox
from src.ui.auth_ui import DogAcademyApp  # Путь к приложению
from database.db_session import init_db, close_sessions  # Функция для закрытия сессий

def on_close():
    """Обработчик закрытия окна."""
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        print("Закрытие игры...")
        close_sessions()  # Закрытие всех сессий перед выходом
        root.quit()  # Завершаем главный цикл приложения
        root.destroy()  # Закрытие окна

def main():
    """Основной запуск приложения."""
    global root
    # Инициализация базы данных
    init_db()

    # Создаем экземпляр приложения
    app = DogAcademyApp(root)
    root.protocol("WM_DELETE_WINDOW", on_close)  # Перехват события закрытия окна
    root.mainloop()  # Запуск основного цикла обработки событий

if __name__ == "__main__":
    root = Tk()  # Создание корневого окна
    main()
