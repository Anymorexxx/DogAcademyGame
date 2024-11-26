import tkinter as tk
from PIL import Image, ImageTk
from src.utils import clear_frame
from config import DOG_CHARACTERS, BACKGROUND_GAME, LOGO, COUNTDOWN_DURATION
from src.user_functions.map_generator import generate_map
from src.user_functions.game_functions import handle_obstacle


class GameUI:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.selected_dog = None
        self.current_level = 1
        self.score = 0

        self.root.configure(bg="lightblue")
        self.create_logo()
        self.show_dog_selection()

    def create_logo(self):
        """Создание логотипа."""
        logo_image = Image.open(LOGO)
        logo_photo = ImageTk.PhotoImage(logo_image.resize((200, 100), Image.Resampling.LANCZOS))
        logo_label = tk.Label(self.root, image=logo_photo, bg="lightblue")
        logo_label.image = logo_photo
        logo_label.pack(pady=10)

    def show_dog_selection(self):
        """Выбор собаки пользователем."""
        clear_frame(self.root)
        tk.Label(
            self.root, text="Выберите собаку", font=("Comic Sans MS", 24), bg="lightblue"
        ).pack(pady=20)

        dog_frame = tk.Frame(self.root, bg="lightblue")
        dog_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Центрируем фрейм

        for breed, details in DOG_CHARACTERS.items():
            dog_image = Image.open(details["image"])
            dog_photo = ImageTk.PhotoImage(dog_image.resize((150, 150), Image.Resampling.LANCZOS))

            # Фрейм для кнопки и подписи
            dog_item = tk.Frame(dog_frame, bg="lightblue")
            dog_item.pack(side=tk.LEFT, padx=15, pady=15)

            # Кнопка с изображением
            button = tk.Button(
                dog_item,
                image=dog_photo,
                command=lambda b=breed: self.confirm_dog_selection(b),
                bg="lightblue",
                borderwidth=0,
            )
            button.image = dog_photo  # Сохраняем ссылку на изображение
            button.pack()

            # Подпись с породой собаки
            tk.Label(
                dog_item,
                text=breed,
                font=("Comic Sans MS", 16),
                bg="lightblue"
            ).pack(pady=5)

    def confirm_dog_selection(self, breed):
        """Подтверждение выбора собаки."""
        self.selected_dog = breed
        self.show_level_selection()

    def show_level_selection(self):
        """Отображение выбора уровня."""
        clear_frame(self.root)
        tk.Label(
            self.root, text="Выберите уровень", font=("Comic Sans MS", 20), bg="lightblue"
        ).pack(pady=10)

        level_frame = tk.Frame(self.root, bg="lightblue")
        level_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Центрируем фрейм

        for level in range(1, 6):  # Доступно 5 уровней
            tk.Button(
                level_frame,
                text=f"Уровень {level}",
                command=lambda l=level: self.start_level(l),
                font=("Comic Sans MS", 16),
                bg="lightgreen",
                width=12,
            ).pack(pady=10)

    def start_level(self, level):
        """Начало выбранного уровня."""
        self.current_level = level
        self.countdown()

    def countdown(self):
        """Обратный отсчёт перед началом уровня."""
        clear_frame(self.root)
        countdown_label = tk.Label(
            self.root, text="", font=("Comic Sans MS", 30), bg="lightblue"
        )
        countdown_label.pack(expand=True)

        for i in range(COUNTDOWN_DURATION, 0, -1):
            countdown_label.config(text=f"{i}...")
            self.root.update()
            self.root.after(1000)

        self.start_game()

    def start_game(self):
        """Запуск игрового процесса."""
        clear_frame(self.root)

        # Генерация карты
        map_data = generate_map(self.current_level)

        for obstacle in map_data:
            result = handle_obstacle(obstacle, self.score, self.root)
            self.score = result["new_score"]

        if self.score >= 10:  # Условие победы
            self.show_victory_screen()

    def show_victory_screen(self):
        """Экран победы."""
        clear_frame(self.root)

        tk.Label(
            self.root, text="Ура, победа!", font=("Comic Sans MS", 30), bg="lightblue"
        ).pack(pady=10)

        dog_image = Image.open(DOG_CHARACTERS[self.selected_dog]["image"])
        dog_photo = ImageTk.PhotoImage(dog_image.resize((150, 150), Image.Resampling.LANCZOS))
        tk.Label(self.root, image=dog_photo, bg="lightblue").pack(pady=10)
        tk.Label(
            self.root,
            text=f"Порода: {self.selected_dog}\nСобрано косточек: {self.score}",
            font=("Comic Sans MS", 20),
            bg="lightblue",
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Вернуться в главное меню",
            command=lambda: self.__init__(self.root, self.user_id),
            font=("Comic Sans MS", 16),
            bg="lightgreen",
        ).pack(pady=10)
