import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from database.models import Questions
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