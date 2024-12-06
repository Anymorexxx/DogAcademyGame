from tkinter import ttk
import tkinter as tk
from src.utils import clear_frame

def add_info(frame):
    """Добавление информации о породах собак."""
    clear_frame(frame)
    tk.Label(frame, text="Добавление информации", font=("Comic Sans MS", 16)).pack()

    # Реализовать интерфейс для добавления данных


def edit_records(frame):
    """Редактирование записей в базе знаний."""
    clear_frame(frame)
    tk.Label(frame, text="Редактирование записей", font=("Comic Sans MS", 16)).pack()

    # Реализовать интерфейс для редактирования записей


def delete_records(frame):
    """Удаление записей из базы знаний."""
    clear_frame(frame)
    tk.Label(frame, text="Удаление записей", font=("Comic Sans MS", 16)).pack()

    # Реализовать интерфейс для удаления данных


def view_knowledge_base(frame):
    """Просмотр базы знаний."""
    clear_frame(frame)
    tk.Label(frame, text="База знаний", font=("Comic Sans MS", 16)).pack()

    table = ttk.Treeview(frame, columns=("Порода", "Описание"), show="headings")
    table.heading("Порода", text="Порода")
    table.heading("Описание", text="Описание")
    table.pack(fill="both", expand=True)

    # Пример данных
    table.insert("", "end", values=("Лабрадор", "Дружелюбная порода"))
    table.insert("", "end", values=("Доберман", "Отличный сторож"))


def generate_questions(frame):
    print("Я по приколу вызвался")
    """Генерация вопросов на основе текстов."""
    clear_frame(frame)
    tk.Label(frame, text="Генерация вопросов", font=("Comic Sans MS", 16)).pack()

    # Реализовать генерацию вопросов

