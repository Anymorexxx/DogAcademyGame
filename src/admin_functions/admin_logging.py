import tkinter as tk
from tkinter import ttk
import csv
from src.utils import clear_frame

def show_logs(frame):
    """Отображение логов действий пользователей."""
    clear_frame(frame)
    tk.Label(frame, text="Логи действий", font=("Comic Sans MS", 16)).pack()

    table = ttk.Treeview(frame, columns=("Время", "Действие", "Пользователь"), show="headings")
    table.heading("Время", text="Время")
    table.heading("Действие", text="Действие")
    table.heading("Пользователь", text="Пользователь")
    table.pack(fill="both", expand=True)

    # Добавьте логи для примера
    table.insert("", "end", values=("2024-11-19 12:30", "Добавление вопроса", "admin"))
    table.insert("", "end", values=("2024-11-19 13:00", "Удаление пользователя", "moderator"))


def export_logs():
    data = [
        ("2024-11-19 12:30", "Добавление вопроса", "admin"),
        ("2024-11-19 13:00", "Удаление пользователя", "moderator"),
    ]
    with open("logs.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Время", "Действие", "Пользователь"])
        writer.writerows(data)
    print("Логи успешно экспортированы в logs.csv")

