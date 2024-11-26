import tkinter as tk
from src.utils import clear_frame
from database.db_events import get_user_progress


def profile_ui(root, user_id):
    """Интерфейс профиля пользователя."""
    clear_frame(root)

    frame = tk.Frame(root, bg="#f8e1e1")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Профиль", font=("Comic Sans MS", 30), bg="#f8e1e1").pack(pady=20)

    # Статистика пользователя
    progress = get_user_progress(user_id)
    levels_completed = len(progress)
    bones_collected = sum([session.score for session in progress])

    stats_text = f"Пройдено уровней: {levels_completed}\nСобрано косточек: {bones_collected}"
    tk.Label(frame, text=stats_text, font=("Comic Sans MS", 20), bg="#f8e1e1").pack(pady=10)

    tk.Button(frame, text="Назад", command=lambda: clear_frame(root), font=("Comic Sans MS", 20)).pack(pady=20)
