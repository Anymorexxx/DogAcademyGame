import tkinter as tk
from tkinter import ttk
import csv
from src.utils import clear_frame
import logging
from datetime import datetime
BACKGROUND_COLOR = "#403d49"
TEXT_COLOR = "#b2acc0"
HEADER_COLOR = "#2f2b38"
BUTTON_COLOR = "#444444"

logging.basicConfig(
    filename="logs/logfile.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def log_action(action, user):
    logging.info(f"{action} - Пользователь: {user}")


def show_logs(frame):
    """Отображение логов действий пользователей в тёмной теме."""
    clear_frame(frame)
    tk.Label(frame, text="Логи действий", font=("Comic Sans MS", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)

    # Настройка таблицы с логами
    table = ttk.Treeview(frame, columns=("Время", "Действие", "Пользователь"), show="headings", style="Dark.Treeview")
    table.heading("Время", text="Время")
    table.heading("Действие", text="Действие")
    table.heading("Пользователь", text="Пользователь")
    table.pack(fill="both", expand=True)

    # Добавление логов для примера
    table.insert("", "end", values=("2024-11-19 12:30", "Добавление вопроса", "admin"))
    table.insert("", "end", values=("2024-11-19 13:00", "Удаление пользователя", "moderator"))

    # Применение стиля к таблице
    style = ttk.Style()
    style.configure("Dark.Treeview", background=BACKGROUND_COLOR, foreground=TEXT_COLOR, fieldbackground=BACKGROUND_COLOR)
    style.configure("Dark.Treeview.Heading", background=HEADER_COLOR, foreground=TEXT_COLOR)

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

