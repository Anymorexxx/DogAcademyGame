import tkinter as tk
from config import (
    BACKGROUND_COLOR_USER,
    TOP_PANEL_COLOR_USER,
    BUTTON_COLOR_PROFILE_USER,
    BUTTON_COLOR_PLAY_USER,
    BUTTON_COLOR_EXIT_USER,
    BUTTON_TEXT_COLOR_USER,
    FONT_USER,
    BIG_FONT_USER,
    BUTTON_RADIUS_USER,
    EXIT_BUTTON_SIZE_USER,
)


class UserApp:
    def __init__(self, root, auth_ui):
        self.root = root
        self.auth_ui = auth_ui
        self.root.configure(bg=BACKGROUND_COLOR_USER)
        self.root.geometry("1920x1080")  # Разрешение окна
        self.root.title("Собачья академия")
        print("Главное меню активно")  # Лог при открытии меню
        self.show_user_dashboard()

    def show_user_dashboard(self):
        """Показать интерфейс пользователя."""
        # Верхняя панель
        top_panel = tk.Frame(self.root, bg=TOP_PANEL_COLOR_USER, height=100)
        top_panel.pack(fill=tk.X, side=tk.TOP)

        # Кнопки на верхней панели
        for text, command in [("Профиль", self.show_profile), ("Магазин", self.show_shop), ("База знаний", self.show_knowledge)]:
            button = tk.Button(
                top_panel,
                text=text,
                bg=BUTTON_COLOR_PROFILE_USER,
                fg=BUTTON_TEXT_COLOR_USER,
                font=FONT_USER,
                relief=tk.FLAT,
                padx=20,
                pady=10,
                command=command,
            )
            button.pack(side=tk.LEFT, padx=20)

        # Кнопка "Играть" в центре
        play_button = tk.Button(
            self.root,
            text="Играть",
            bg=BUTTON_COLOR_PLAY_USER,
            fg=BUTTON_TEXT_COLOR_USER,
            font=BIG_FONT_USER,
            relief=tk.FLAT,
            height=2,
            width=10,
            command=self.play_game,
        )
        play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Кнопка "Выход" в правом нижнем углу
        exit_button = tk.Button(
            self.root,
            text="Выход",
            bg=BUTTON_COLOR_EXIT_USER,
            fg=BUTTON_TEXT_COLOR_USER,
            font=FONT_USER,
            width=EXIT_BUTTON_SIZE_USER[0] // 10,
            height=EXIT_BUTTON_SIZE_USER[1] // 10,
            command=self.exit_app,
        )
        exit_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor=tk.SE)

    def play_game(self):
        """Заглушка для игры."""
        print("Запуск игры...")

    def exit_app(self):
        """Заглушка для выхода."""
        print("Приложение закрыто")
        self.root.quit()

    def show_profile(self):
        """Заглушка для профиля."""
        print("Переход в профиль...")

    def show_shop(self):
        """Заглушка для магазина."""
        print("Переход в магазин...")

    def show_knowledge(self):
        """Заглушка для базы знаний."""
        print("Переход в базу знаний...")
