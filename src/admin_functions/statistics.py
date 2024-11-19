import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.utils import clear_frame

def show_statistics(frame):
    """Отображение статистики пользователей и уровней."""
    clear_frame(frame)
    tk.Label(frame, text="Статистика пользователей", font=("Comic Sans MS", 16)).pack()

    # Пример: график с количеством пользователей
    fig, ax = plt.subplots()
    ax.bar(["Level 1", "Level 2", "Level 3"], [10, 15, 8])  # Пример данных
    ax.set_title("Популярность уровней")
    ax.set_xlabel("Уровни")
    ax.set_ylabel("Количество прохождений")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()



