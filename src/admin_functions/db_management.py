import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from database.models import Questions, Notifications
from database.db_session import engine
from src.utils import clear_frame

Session = sessionmaker(bind=engine)

def view_tables():
    # Пример функции, которая будет выводить информацию о таблицах
    print("Отображаем таблицы базы данных.")

def edit_users():
    # Код для редактирования пользователей
    pass

def manage_questions(frame):
    """Функция для управления вопросами."""
    clear_frame(frame)

    tk.Label(frame, text="Управление вопросами", font=("Comic Sans MS", 16)).pack()

    session = Session()
    questions = session.query(Questions).all()

    table = ttk.Treeview(frame, columns=("ID", "Вопрос", "Ответ"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Вопрос", text="Вопрос")
    table.heading("Ответ", text="Ответ")
    table.pack(fill="both", expand=True)

    for question in questions:
        table.insert("", "end", values=(question.id, question.text, question.answer))

    session.close()

def add_user_to_db(user_data, root):
    # Логика добавления пользователя в базу данных
    try:
        # Пример кода для добавления в базу (зависит от реализации вашей базы данных)
        # db_session.add(user_data)
        # db_session.commit()

        # Если добавление прошло успешно
        notification = Notifications(root)
        notification.show_info("Успех", f"Пользователь {user_data['username']} успешно добавлен!")

    except Exception as e:
        # Если возникла ошибка
        notification = Notifications(root)
        notification.show_error("Ошибка", f"Ошибка при добавлении пользователя: {str(e)}")