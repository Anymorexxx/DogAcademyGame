import tkinter as tk
from src.utils import clear_frame

def manage_levels(frame):
    """Создание и настройка уровней."""
    clear_frame(frame)
    tk.Label(frame, text="Создание и настройка уровней", font=("Comic Sans MS", 16)).pack()

    # Добавить интерфейс для добавления уровней


def manage_dog_params(frame):
    """Настройка параметров собаки."""
    clear_frame(frame)
    tk.Label(frame, text="Настройка параметров собаки", font=("Comic Sans MS", 16)).pack()

    # Добавить поля для параметров, например, здоровье, голод, сонливость