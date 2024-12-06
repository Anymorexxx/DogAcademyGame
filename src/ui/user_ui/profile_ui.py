import tkinter as tk
from src.utils import clear_frame
from database.db_events import get_user_progress, get_user_by_id


def profile_ui(root, user_id, user_app):
    """Интерфейс профиля пользователя."""
    clear_frame(root)

    frame = tk.Frame(root, bg="#f8e1e1")
    frame.pack(fill=tk.BOTH, expand=True)

    # Обновляем данные пользователя из базы
    user = get_user_by_id(user_id)
    if not user:
        username = "Неизвестный пользователь"
        levels_completed = 0
        bones_collected = 0
    else:
        username = user.username
        progress = get_user_progress(user_id)
        levels_completed = len({session.level for session in progress if session.score > 0})
        bones_collected = sum(session.score for session in progress)

    tk.Label(
        frame,
        text=f"Профиль: {username}",
        font=("Comic Sans MS", 30),
        bg="#f8e1e1",
    ).pack(pady=20)

    stats_text = f"Пройдено уровней: {levels_completed}\nСобрано косточек: {bones_collected}"
    tk.Label(frame, text=stats_text, font=("Comic Sans MS", 20), bg="#f8e1e1").pack(pady=10)

    # Кнопка "Назад"
    back_button = tk.Button(
        frame,
        text="Назад",
        command=lambda: [clear_frame(root), user_app.show_user_dashboard()],
        font=("Comic Sans MS", 20)
    )
    back_button.pack(pady=20)

