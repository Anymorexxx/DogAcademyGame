import tkinter as tk
from tkinter import messagebox


def clear_frame(frame):
    """Удаление всех виджетов из фрейма."""
    for widget in frame.winfo_children():
        widget.destroy()

def feature_in_development(frame):
    """Сообщение о том, что функционал недоступен."""
    clear_frame(frame)  # Очистка фрейма перед выводом сообщения
    tk.Label(
        frame,
        text="Этот функционал пока что недоступен, в разработке.",
        bg="#403d49",  # Фон сообщения
        fg="#b2acc0",  # Цвет текста
        font=("Comic Sans MS", 16)
    ).pack(expand=True)

def show_message(message):
    """Показать сообщение пользователю"""
    message_window = tk.Toplevel()
    message_label = tk.Label(message_window, text=message, font=("Comic Sans MS", 16))
    message_label.pack(pady=20)
    ok_button = tk.Button(message_window, text="OK", command=message_window.destroy)
    ok_button.pack(pady=10)