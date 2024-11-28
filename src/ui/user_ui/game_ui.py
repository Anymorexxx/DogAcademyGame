import tkinter as tk
from PIL import Image, ImageTk
import random
import logging

from database.db_events import get_user_by_id
from src.user_functions.game_logs import setup_logging
from config import DOG_CHARACTERS, DONE, BONE, BACKGROUND_GAME
from src.utils import clear_frame

# Настройка логирования
setup_logging()

class GameUI:
    def __init__(self, root, user_id, return_to_main_menu_callback):
        self.root = root
        self.user_id = user_id
        self.return_to_main_menu_callback = return_to_main_menu_callback
        self.selected_dog = None
        self.current_level = 1
        self.max_unlocked_level = 1
        self.completed_levels = set()

        self.total_bones = 0
        self.dog_position = [1, 1]
        self.map_canvas = None
        self.bones_positions = []
        self.max_bones_per_level = 10
        self.steps_taken = 0

        # Изображения
        self.done_image = ImageTk.PhotoImage(Image.open(DONE).resize((50, 50), Image.Resampling.LANCZOS))
        self.bones_photo = ImageTk.PhotoImage(Image.open(BONE).resize((50, 50), Image.Resampling.LANCZOS))

        # Размер сетки
        self.grid_size = 60
        self.cols = 32
        self.rows = 18

        # Настройки окна
        self.root.geometry("1920x1080")
        self.root.configure(bg="#E5E5E5")

        # Привязка клавиш
        self.root.bind("<KeyPress-w>", self.move_up)
        self.root.bind("<KeyPress-s>", self.move_down)
        self.root.bind("<KeyPress-a>", self.move_left)
        self.root.bind("<KeyPress-d>", self.move_right)
        self.root.bind("<Escape>", self.on_escape)

        # Отображение начального экрана
        self.show_dog_selection()

    def create_background(self):
        """Создаёт фон для игры."""
        try:
            bg_image = Image.open(BACKGROUND_GAME)
            bg_photo = ImageTk.PhotoImage(bg_image.resize((1920, 1080), Image.Resampling.LANCZOS))
            bg_label = tk.Label(self.root, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            logging.error(f"Ошибка загрузки фона: {e}")

    def show_dog_selection(self):
        """Отображение выбора собаки пользователем."""
        clear_frame(self.root)
        self.create_background()

        tk.Label(
            self.root, text="Выберите собаку", font=("Comic Sans MS", 24), bg="#E5E5E5"
        ).pack(pady=20)

        dog_frame = tk.Frame(self.root, bg="#E5E5E5")
        dog_frame.pack(pady=50)

        dog_size = 150
        for breed, details in DOG_CHARACTERS.items():
            try:
                dog_image = Image.open(details["image"]).resize((dog_size, dog_size), Image.Resampling.LANCZOS)
                dog_photo = ImageTk.PhotoImage(dog_image)

                dog_container = tk.Frame(dog_frame, bg="#E5E5E5")
                dog_container.pack(side=tk.LEFT, padx=15)

                button = tk.Button(
                    dog_container,
                    image=dog_photo,
                    command=lambda b=breed: self.confirm_dog_selection(b),
                    bg="#E5E5E5",
                    borderwidth=0,
                )
                button.image = dog_photo
                button.pack()

                tk.Label(dog_container, text=breed, font=("Comic Sans MS", 14), bg="#E5E5E5").pack()

            except Exception as e:
                logging.error(f"Ошибка загрузки изображения для собаки {breed}: {e}")

        tk.Button(
            self.root,
            text="Вернуться",
            font=("Comic Sans MS", 16),
            bg="lightgreen",
            command=self.return_to_main_menu_callback,
        ).place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def confirm_dog_selection(self, breed):
        """Подтверждение выбора собаки."""
        self.selected_dog = breed
        self.show_level_selection()

    def show_level_selection(self):
        """Отображение выбора уровня."""
        clear_frame(self.root)
        self.create_background()

        tk.Label(
            self.root, text="Выберите уровень", font=("Comic Sans MS", 24), bg="#E5E5E5"
        ).pack(pady=20)

        level_frame = tk.Frame(self.root, bg="#E5E5E5")
        level_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for level in range(1, 6):
            button = tk.Button(
                level_frame,
                text=f"Уровень {level}",
                state=tk.NORMAL if level <= self.max_unlocked_level else tk.DISABLED,
                font=("Comic Sans MS", 20),
                bg="#4CAF50" if level <= self.max_unlocked_level else "#A9A9A9",
                width=15,
                height=2,
                command=lambda l=level: self.start_level(l),
            )
            button.pack(pady=10)

        tk.Button(
            self.root,
            text="Вернуться",
            font=("Comic Sans MS", 16),
            bg="lightgreen",
            command=self.show_dog_selection,
        ).place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def start_level(self, level):
        """Начало выбранного уровня."""
        self.current_level = level
        self.countdown()

    def countdown(self):
        """Обратный отсчёт перед началом уровня."""
        clear_frame(self.root)
        countdown_label = tk.Label(
            self.root, text="", font=("Comic Sans MS", 30), bg="#E5E5E5"
        )
        countdown_label.pack(expand=True)

        for i in range(3, 0, -1):
            countdown_label.config(text=f"{i}...")
            self.root.update()
            self.root.after(1000)

        self.start_game()

    def start_game(self):
        """Запуск игрового процесса."""
        clear_frame(self.root)
        self.map_canvas = tk.Canvas(self.root, width=1920, height=1080, bg="#E5E5E5")
        self.map_canvas.pack()

        self.draw_grid()
        self.bones_positions = self.generate_bones()

        # Прямоугольник и изображение косточек (создаются один раз)
        self.rect_x1, self.rect_y1 = 1600, 0
        self.rect_x2, self.rect_y2 = self.rect_x1 + 180, 100
        self.map_canvas.create_rectangle(
            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, fill="#CCCCCC", outline="#CCCCCC", tags="rect"
        )
        self.map_canvas.create_image(1650, 50, image=self.bones_photo, tags="rect")
        self.bones_label = tk.Label(self.root, text=f"{self.total_bones}", font=("Comic Sans MS", 16), bg="#CCCCCC")
        self.bones_label.place(x=1700, y=30)

        # В методе update_map (не удаляем прямоугольник):
        self.map_canvas.delete("all")  # Удаляем только динамичные объекты карты (косточки, собаку)
        self.draw_grid()
        self.collect_bones()

        self.update_map()  # Начальное обновление карты

    def draw_grid(self):
        """Рисует сетку для движения."""
        for x in range(0, 1920, self.grid_size):
            self.map_canvas.create_line(x, 0, x, 1080, fill="lightgray")
        for y in range(0, 1080, self.grid_size):
            self.map_canvas.create_line(0, y, 1920, y, fill="lightgray")

    def generate_bones(self):
        """Генерация косточек на карте."""
        return [
            (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            for _ in range(2)
        ]

    def collect_bones(self):
        """Проверка и сбор косточек."""
        for bone in self.bones_positions[:]:
            if self.dog_position == [bone[0], bone[1]]:
                self.bones_positions.remove(bone)
                self.total_bones += 1
                self.bones_label.config(text=f"{self.total_bones}")

        if self.steps_taken % 10 == 0 and len(self.bones_positions) < self.max_bones_per_level:
            self.bones_positions.extend(self.generate_bones())

    def move_up(self, event):
        """Движение вверх."""
        self.root.focus_force()
        if self.dog_position[1] > 0:
            self.dog_position[1] -= 1
        self.steps_taken += 1
        self.update_map()

    def move_down(self, event):
        """Движение вниз."""
        self.root.focus_force()
        if self.dog_position[1] < self.rows - 1:
            self.dog_position[1] += 1
        self.steps_taken += 1
        self.update_map()

    def move_left(self, event):
        """Движение влево."""
        self.root.focus_force()
        if self.dog_position[0] > 0:
            self.dog_position[0] -= 1
        self.steps_taken += 1
        self.update_map()

    def move_right(self, event):
        """Движение вправо."""
        self.root.focus_force()
        if self.dog_position[0] < self.cols - 1:
            self.dog_position[0] += 1
        self.steps_taken += 1
        self.update_map()

    def on_escape(self, event):
        """Обработчик для нажатия клавиши ESC."""
        self.show_pause_menu()

        def show_pause_menu(self):
            """Создание окна паузы."""
            pause_window = tk.Toplevel(self.root)
            pause_window.title("Пауза")
            pause_window.geometry("400x200")
            pause_window.configure(bg="#E5E5E5")
            pause_window.grab_set()  # Блокируем взаимодействие с основным окном

            # Кнопка "Сохранить и выйти"
            save_exit_button = tk.Button(
                pause_window,
                text="Сохранить и выйти",
                font=("Comic Sans MS", 16),
                bg="#FF6347",
                command=self.save_and_exit
            )
            save_exit_button.pack(pady=20)

            # Кнопка "Продолжить"
            continue_button = tk.Button(
                pause_window,
                text="Продолжить",
                font=("Comic Sans MS", 16),
                bg="#4CAF50",
                command=pause_window.destroy
            )
            continue_button.pack(pady=20)

    def show_pause_menu(self):
        """Создание окна паузы."""
        pause_window = tk.Toplevel(self.root)
        pause_window.title("Пауза")
        pause_window.geometry("400x200")
        pause_window.configure(bg="#E5E5E5")
        pause_window.grab_set()  # Блокируем взаимодействие с основным окном

        # Кнопка "Сохранить и выйти"
        save_exit_button = tk.Button(
            pause_window,
            text="Сохранить и выйти",
            font=("Comic Sans MS", 16),
            bg="#FF6347",
            command=self.save_and_exit  # Этот метод теперь определён
        )
        save_exit_button.pack(pady=20)

        # Кнопка "Продолжить"
        continue_button = tk.Button(
            pause_window,
            text="Продолжить",
            font=("Comic Sans MS", 16),
            bg="#4CAF50",
            command=pause_window.destroy
        )
        continue_button.pack(pady=20)

    def save_and_exit(self):
        """Сохранение данных и выход в главное меню."""
        logging.info("Сохранение прогресса: уровень %d, собрано косточек %d.", self.current_level, self.total_bones)
        # Дополнительно можно добавить сохранение прогресса в базу данных.
        # Пример:
        # save_progress_to_database(user_id=self.user_id, level=self.current_level, bones=self.total_bones)
        self.return_to_main_menu_callback()  # Возврат в главное меню

    def update_map(self):
        """Обновление карты."""
        self.map_canvas.delete("all")
        self.draw_grid()

        # Отображение косточек
        for x, y in self.bones_positions:
            self.map_canvas.create_image(
                x * self.grid_size + self.grid_size // 2,
                y * self.grid_size + self.grid_size // 2,
                image=self.bones_photo
            )

        # Отображение собаки
        dog_image = Image.open(DOG_CHARACTERS[self.selected_dog]["image"]).resize((self.grid_size, self.grid_size),
                                                                                  Image.Resampling.LANCZOS)
        self.dog_photo = ImageTk.PhotoImage(dog_image)
        self.map_canvas.create_image(
            self.dog_position[0] * self.grid_size + self.grid_size // 2,
            self.dog_position[1] * self.grid_size + self.grid_size // 2,
            image=self.dog_photo
        )

        # Проверка сбора косточек
        self.collect_bones()

        # Условие перехода на следующий уровень
        target_bones = 10 * (2 ** (self.current_level - 1))  # Геометрическая прогрессия
        if self.total_bones >= target_bones:
            self.show_victory_screen()

    def show_victory_screen(self):
        """Экран победы."""
        victory_window = tk.Toplevel(self.root)
        victory_window.title("Ура, победа!")
        victory_window.geometry("800x600")
        victory_window.configure(bg="#E5E5E5")
        victory_window.grab_set()

        # Изображение собаки
        dog_image = Image.open(DOG_CHARACTERS[self.selected_dog]["image"]).resize((200, 200), Image.Resampling.LANCZOS)
        dog_photo = ImageTk.PhotoImage(dog_image)
        dog_label = tk.Label(victory_window, image=dog_photo, bg="#E5E5E5")
        dog_label.image = dog_photo
        dog_label.place(x=50, y=50)

        # Текст победы
        victory_label = tk.Label(
            victory_window, text="Ура, победа!", font=("Comic Sans MS", 24), bg="#E5E5E5"
        )
        victory_label.pack(pady=20)

        # Характеристики собаки
        dog_info = f"Порода: {self.selected_dog}"
        info_label = tk.Label(
            victory_window, text=dog_info, font=("Comic Sans MS", 16), bg="#E5E5E5"
        )
        info_label.place(x=300, y=100)

        # Собрано косточек
        target_bones = 10 * (2 ** (self.current_level - 1))  # Геометрическая прогрессия для косточек
        collected_info = f"Собрано: {self.total_bones} из {target_bones}"
        score_label = tk.Label(
            victory_window, text=collected_info, font=("Comic Sans MS", 16), bg="#E5E5E5"
        )
        score_label.place(x=300, y=150)

        # Кнопка перехода на следующий уровень
        next_level_button = tk.Button(
            victory_window, text="Следующий уровень", font=("Comic Sans MS", 16), bg="#4CAF50",
            command=lambda: [victory_window.destroy(), self.start_next_level()]
        )
        next_level_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def start_next_level(self):
        """Переход на следующий уровень и сохранение прогресса."""
        # Сохранение прогресса
        self.save_progress()

        # Переход на следующий уровень
        self.current_level += 1
        self.total_bones = 0  # Сбрасываем счётчик косточек
        self.start_level(self.current_level)

    def save_progress(self):
        """Сохранение прогресса в базе данных."""
        from database.db_events import save_progress, update_user_dog
        from database.db_events import get_user_by_id

        # Получаем информацию о пользователе
        user = get_user_by_id(self.user_id)
        if not user:
            logging.error(f"Пользователь с ID {self.user_id} не найден в базе данных.")
            return  # Прерываем выполнение, если пользователь не найден

        # Сохраняем прогресс текущего уровня
        save_progress(self.user_id, self.current_level, self.total_bones, 0, 100, 0, 0)

        # Получаем уровень и собаку
        dog_id = user.dog_id  # Получаем id собаки пользователя
        update_user_dog(self.user_id, dog_id)  # Сохраняем собаку в профиль
