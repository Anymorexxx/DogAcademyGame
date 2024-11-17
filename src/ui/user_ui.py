import tkinter as tk
from config import BACKGROUND_COLOR, PRIMARY_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, FONT

class UserApp:
    def __init__(self, root, dog_academy_app):
        self.root = root
        self.dog_academy_app = dog_academy_app  # Сохраняем ссылку на DogAcademyApp
        self.show_user_dashboard()

    def show_user_dashboard(self):
        """Показать интерфейс пользователя."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        # Заголовок
        title = tk.Label(
            self.current_frame,
            text="Главное меню",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=FONT,
        )
        title.pack(pady=50)

        # Кнопка "Играть"
        play_button = tk.Button(
            self.current_frame,
            text="Играть",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.play_game,
        )
        play_button.pack(pady=20)

        # Кнопка "Выход"
        logout_button = tk.Button(
            self.current_frame,
            text="Выход",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.dog_academy_app.show_main_menu,  # Вызываем метод из DogAcademyApp
        )
        logout_button.pack(pady=20)

    def play_game(self):
        """Запуск игры."""
        # TODO: Логика игры
        pass

    def clear_frame(self):
        """Очистить текущий фрейм."""
        if hasattr(self, 'current_frame') and self.current_frame:
            self.current_frame.destroy()
