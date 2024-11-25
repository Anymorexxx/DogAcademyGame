import tkinter as tk

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

def create_tooltip(widget, text):
    """Создание подсказки для виджета."""
    tooltip = tk.Toplevel()
    tooltip.wm_overrideredirect(True)  # Отключаем рамки окна
    tooltip.wm_geometry(f"+{widget.winfo_rootx() + 20}+{widget.winfo_rooty() + 20}")
    label = tk.Label(tooltip, text=text, bg="#333", fg="#fff", font=("Comic Sans MS", 10), padx=5, pady=5)
    label.pack()

    def hide_tooltip(event):
        tooltip.destroy()

    widget.bind("<Enter>", lambda event: tooltip.deiconify())
    widget.bind("<Leave>", hide_tooltip)
