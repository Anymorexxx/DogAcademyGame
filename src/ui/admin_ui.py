# admin_ui.py
import tkinter as tk
from config import BACKGROUND_COLOR, PRIMARY_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, FONT

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.show_admin_dashboard()

    def show_admin_dashboard(self):
        """Показать интерфейс администратора."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        # Заголовок
        title = tk.Label(
            self.current_frame,
            text="Админ-Панель",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=FONT,
        )
        title.pack(pady=50)

        # Кнопка для управления вопросами
        manage_questions_button = tk.Button(
            self.current_frame,
            text="Управление вопросами",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.manage_questions,
        )
        manage_questions_button.pack(pady=20)

        # Кнопка для управления пользователями
        manage_users_button = tk.Button(
            self.current_frame,
            text="Управление пользователями",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.manage_users,
        )
        manage_users_button.pack(pady=20)

    def manage_questions(self):
        """Управление вопросами в игре."""
        pass

    def manage_users(self):
        """Управление пользователями игры."""
        pass

    def clear_frame(self):
        """Очистить текущий фрейм."""
        if hasattr(self, 'current_frame') and self.current_frame:
            self.current_frame.destroy()
