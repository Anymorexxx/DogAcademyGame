from tkinter import Tk
from tkinter import messagebox
from src.ui.auth_ui import DogAcademyApp  # Изменил на правильный путь
from database.db_session import init_db

def on_close():
    """Обработчик закрытия окна."""
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.destroy()

def main():
    """Основной запуск приложения."""
    global root
    # Инициализируем базу данных
    init_db()

    # Запускаем графический интерфейс
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_close)
    app = DogAcademyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
