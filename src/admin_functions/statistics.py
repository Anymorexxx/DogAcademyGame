import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.utils import clear_frame
from database.db_session import get_session
from sqlalchemy.sql import func
from database.models import Users, GameSession, Questions  # Пример моделей

def show_statistics(frame):
    """Отображение статистики."""
    clear_frame(frame)
    tk.Label(frame, text="Статистика", font=("Comic Sans MS", 16), bg="#403d49", fg="#b2acc0").pack(pady=10)

    # Таблица с общей статистикой
    table = ttk.Treeview(frame, columns=("Metric", "Value"), show="headings", height=5)
    table.heading("Metric", text="Параметр")
    table.heading("Value", text="Значение")
    table.pack(pady=10, padx=20, fill="x", expand=True)

    # Получение данных для таблицы
    stats = gather_statistics()
    for metric, value in stats.items():
        table.insert("", tk.END, values=(metric, value))

    # График активности пользователей
    tk.Label(frame, text="Активность пользователей", font=("Comic Sans MS", 14), bg="#403d49", fg="#b2acc0").pack(pady=10)

    fig, ax = plt.subplots(figsize=(6, 4))
    time_labels, activity_values = get_user_activity()
    ax.plot(time_labels, activity_values, marker="o")
    ax.set_title("Активность пользователей по времени")
    ax.set_xlabel("Время")
    ax.set_ylabel("Количество действий")
    ax.grid()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

def gather_statistics():
    """Собирает основные метрики для таблицы статистики."""
    session = get_session()

    # Количество зарегистрированных пользователей
    user_count = session.query(Users).count()

    # Популярные уровни
    level_data = session.query(GameSession.level, func.count(GameSession.session_id)).group_by(GameSession.level).all()
    popular_levels = sorted(level_data, key=lambda x: x[1], reverse=True)[:3]

    # Трудные вопросы
    question_data = session.query(Questions.question_text, Questions.incorrect_attempts).order_by(Questions.incorrect_attempts.desc()).all()
    hardest_questions = question_data[:3]

    # Средняя продолжительность игры
    avg_duration = session.query(func.avg(GameSession.duration)).scalar() or 0

    # Состояние базы данных
    db_size = get_database_size()

    session.close()

    return {
        "Количество пользователей": user_count,
        "Популярные уровни": ", ".join([f"Уровень {lvl} ({cnt} раз)" for lvl, cnt in popular_levels]),
        "Трудные вопросы": ", ".join([f"'{text}' ({cnt} ошибок)" for text, cnt in hardest_questions]),
        "Средняя продолжительность игры": f"{avg_duration:.2f} секунд",
        "Объем базы данных": f"{db_size} КБ"
    }

def get_user_activity():
    """Генерирует данные для графика активности пользователей."""
    session = get_session()
    activity_data = session.query(GameSession.start_time).all()

    activity_by_hour = {}
    for time in activity_data:
        hour = time.start_time.hour
        activity_by_hour[hour] = activity_by_hour.get(hour, 0) + 1

    session.close()

    if not activity_by_hour:
        return ["Нет данных"], [0]

    hours = sorted(activity_by_hour.keys())
    activity = [activity_by_hour[hour] for hour in hours]
    hours = [f"{hour}:00" for hour in hours]
    return hours, activity

def get_database_size():
    """Возвращает размер базы данных в КБ."""
    import os
    db_path = "database/db.sqlite"
    if os.path.exists(db_path):
        return round(os.path.getsize(db_path) / 1024, 2)
    return 0
