import time
import tkinter as tk
from src.utils import clear_frame
from database.db_events import save_progress


def start_game(root, user_id, dog_id):
    """Игровой процесс."""
    clear_frame(root)

    # Обратный отсчет
    for i in range(3, 0, -1):
        clear_frame(root)
        tk.Label(root, text=f"{i}...", font=("Comic Sans MS", 30)).pack(expand=True)
        root.update()
        time.sleep(1)  # Пауза между отсчетами

    # Начало уровня
    print("Начало уровня")  # Для отладки

    # Здесь подключается логика работы с картой и вопросами
    pass


def handle_checkpoint(obstacle, current_score, root):
    """
    Обрабатывает чек-поинт (косточку).
    obstacle - данные о текущем препятствии
    current_score - текущий счёт
    root - корневой элемент
    """
    # Пример вопроса
    question = "Как ухаживать за собакой?"
    correct_answer = "Кормить и гулять"

    # Окно для вопроса
    question_window = tk.Toplevel(root)
    question_window.title("Вопрос")

    question_label = tk.Label(question_window, text=question, font=("Comic Sans MS", 14))
    question_label.pack(pady=10)

    answer_var = tk.StringVar()
    answer_entry = tk.Entry(question_window, textvariable=answer_var, font=("Comic Sans MS", 14))
    answer_entry.pack(pady=10)

    def submit_answer():
        nonlocal current_score  # Используем nonlocal для изменения current_score в замыканиях
        answer = answer_var.get().strip().lower()
        if answer == correct_answer.lower():
            current_score += 1  # За правильный ответ добавляется 1 косточка
        else:
            current_score -= 1  # Штраф за неправильный ответ

        question_window.destroy()
        return current_score  # Возвращаем обновленный счёт

    submit_button = tk.Button(question_window, text="Ответить", command=submit_answer, font=("Comic Sans MS", 14))
    submit_button.pack(pady=10)

    return current_score
