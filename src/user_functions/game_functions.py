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
        time.sleep(1)

    # Начало уровня
    # Здесь подключается логика работы с картой и вопросами
    pass


def handle_obstacle(obstacle, current_score, root):
    """
    Обработка препятствия (вопроса) с использованием окна.
    Возвращает новый счёт игрока.
    """
    result = {"new_score": current_score}

    def submit_answer():
        user_answer = answer_var.get().strip().lower()
        if user_answer == "правильно":  # Условие для правильного ответа
            result["new_score"] += 1
        else:
            result["new_score"] -= 1
        question_window.destroy()  # Закрываем окно вопроса

    # Создаём новое окно для вопроса
    question_window = tk.Toplevel(root)
    question_window.title("Вопрос")
    question_window.geometry("400x200")

    # Отображение текста вопроса
    tk.Label(question_window, text=f"Вопрос сложности {obstacle['difficulty']}:", font=("Arial", 14)).pack(pady=10)

    # Поле ввода ответа
    answer_var = tk.StringVar()
    tk.Entry(question_window, textvariable=answer_var, font=("Arial", 12)).pack(pady=10)

    # Кнопка подтверждения ответа
    tk.Button(question_window, text="Ответить", command=submit_answer).pack(pady=10)

    # Ожидаем закрытия окна
    question_window.grab_set()  # Блокируем основное окно
    root.wait_window(question_window)  # Ждём завершения окна вопроса

    return result
