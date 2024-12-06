import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
import random
import logging
from database.db_events import get_user_by_id, get_user_progress
from database.info.GameSessions_table import save_game_session
from src.user_functions.game_logs import setup_logging
from config import DOG_CHARACTERS, DONE, BONE, BACKGROUND_GAME
from src.utils import clear_frame

# Настройка логирования
setup_logging()

user = get_user_by_id(user_id=1)
if user:
    print(f"Данные пользователя: {user}")
else:
    print("Пользователь не найден")

class GameUI:
    def __init__(self, root, user_id, return_to_main_menu_callback):
        if not user_id:
            raise ValueError("user_id отсутствует при инициализации GameUI!")

        self.root = root
        self.user_id = user_id
        self.return_to_main_menu_callback = return_to_main_menu_callback
        self.selected_dog = None
        self.current_level = 1
        self.completed_levels = set()

        self.total_bones = 0
        self.dog_position = [1, 1]
        self.map_canvas = None
        self.bones_positions = []
        self.max_bones_per_level = 10
        self.steps_taken = 0
        self.user_data = get_user_by_id(self.user_id)

        # Получаем прогресс пользователя
        self.user_progress = get_user_progress(user_id)
        self.max_unlocked_level = max([session.level for session in self.user_progress]) if self.user_progress else 1

        # Добавляем атрибут is_replay
        self.is_replay = False  # По умолчанию нет повторного прохождения

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

        # Флаги
        self.is_pause_menu_open = False
        self.is_victory_screen_open = False
        self.is_game_active = False

        # Привязка клавиш
        self.root.bind("<KeyPress-w>", self.move_up)
        self.root.bind("<KeyPress-s>", self.move_down)
        self.root.bind("<KeyPress-a>", self.move_left)
        self.root.bind("<KeyPress-d>", self.move_right)
        self.root.bind("<Escape>", self.on_escape)

        # Отображение начального экрана
        self.show_dog_selection()

        if self.user_data:
            self.max_unlocked_level = self.user_data.level or 1
            self.total_bones = sum([session.score for session in get_user_progress(self.user_id)])
        else:
            logging.warning("Данные пользователя не найдены")

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

        tk.Label(self.root, text="Выберите уровень", font=("Comic Sans MS", 24), bg="#E5E5E5").pack(pady=20)

        self.level_frame = tk.Frame(self.root, bg="#E5E5E5")
        self.level_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        progress = get_user_progress(self.user_id)
        self.completed_levels = {session.level for session in progress if session.score > 0}
        self.max_unlocked_level = max(self.completed_levels) + 1 if self.completed_levels else 1

        for level in range(1, 101):
            color = (
                "#4CAF50" if level in self.completed_levels else
                "#FFEB3B" if level == self.max_unlocked_level else
                "#A9A9A9"
            )
            state = tk.NORMAL if level <= self.max_unlocked_level else tk.DISABLED

            button = tk.Button(
                self.level_frame,
                text=f"Уровень {level}",
                bg=color,
                state=state,
                font=("Comic Sans MS", 14),
                command=lambda l=level: self.handle_level_selection(l)
            )
            button.grid(row=(level - 1) // 10, column=(level - 1) % 10, padx=5, pady=5)

        self.update_level_buttons()  # Обновляем кнопки уровней

        tk.Button(
            self.root,
            text="Вернуться",
            font=("Comic Sans MS", 16),
            bg="lightgreen",
            command=self.show_dog_selection
        ).place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def handle_level_selection(self, level):
        """Обработка выбора уровня."""
        if level in self.completed_levels:
            if messagebox.askyesno("Повторить уровень", f"Вы уже прошли уровень {level}. Хотите пройти его заново?"):
                self.is_replay = True
                self.current_level = level
                self.countdown()  # Обратный отсчёт перед началом уровня
        elif level <= self.max_unlocked_level:
            self.current_level = level
            self.is_replay = False
            self.countdown()  # Запуск обратного отсчёта перед началом игры
        else:
            messagebox.showinfo("Недоступно", "Пройдите предыдущие уровни, чтобы разблокировать этот.")

    def update_level_buttons(self):
        """Обновление цветов и состояния кнопок уровней."""
        if not hasattr(self, 'level_frame') or not self.level_frame.winfo_exists():
            return

        for widget in self.level_frame.winfo_children():
            if isinstance(widget, tk.Button):
                level = int(widget['text'].split()[-1])  # Получаем номер уровня из текста кнопки
                # Определяем цвет и состояние кнопки
                if level in self.completed_levels:
                    color = "#4CAF50"  # Зелёный - завершённый уровень
                    state = tk.NORMAL
                elif level == self.max_unlocked_level:
                    color = "#FFEB3B"  # Жёлтый - текущий открытый уровень
                    state = tk.NORMAL
                else:
                    color = "#A9A9A9"  # Серый - заблокированный уровень
                    state = tk.DISABLED

                widget.config(bg=color, state=state)

    def start_level(self, level):
        """Запуск уровня."""
        if level in self.completed_levels:
            if messagebox.askyesno("Повторить уровень", f"Вы уже прошли уровень {level}. Хотите пройти его заново?"):
                self.current_level = level
                self.total_bones = 0
                self.steps_taken = 0
                self.start_game()  # Запускаем уровень заново
            return
        elif level <= self.max_unlocked_level:
            self.current_level = level
            self.countdown()  # Запуск обратного отсчёта перед началом игры
        else:
            messagebox.showinfo("Недоступно", "Этот уровень заблокирован.")

    def countdown(self):
        """Обратный отсчёт перед началом уровня с анимацией."""
        clear_frame(self.root)  # Очищаем экран
        countdown_label = tk.Label(
            self.root, text="Готовьтесь!", font=("Comic Sans MS", 40), bg="#E5E5E5"
        )
        countdown_label.pack(expand=True)

        def update_countdown(counter):
            if counter > 0:
                countdown_label.config(text=f"{counter}", fg=random.choice(["red", "green", "blue"]))
                self.root.update()
                self.root.after(1000, update_countdown, counter - 1)
            else:
                countdown_label.config(text="Вперёд!", fg="orange")
                self.root.update()
                self.root.after(1000, lambda: self.start_game(is_replay=self.is_replay))

        update_countdown(3)  # Старт обратного отсчёта с 3 секунд

    def start_game(self, is_replay=False):
        """Запуск игрового процесса."""
        self.is_replay = is_replay
        logging.info(f"Игра начата на уровне {self.current_level}, повторное прохождение: {self.is_replay}")
        clear_frame(self.root)
        self.map_canvas = tk.Canvas(self.root, width=1920, height=1080, bg="#E5E5E5")
        self.map_canvas.pack()

        self.draw_grid()

        # Сбрасываем состояние уровня
        self.total_bones = 0
        self.steps_taken = 0
        self.dog_position = [1, 1]

        # Генерация косточек, идентично первому запуску
        self.bones_positions = self.generate_bones()

        # Обновление интерфейса
        self.rect_x1, self.rect_y1 = 1600, 0
        self.rect_x2, self.rect_y2 = self.rect_x1 + 180, 100
        self.map_canvas.create_rectangle(
            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, fill="#CCCCCC", outline="#CCCCCC", tags="rect"
        )
        self.map_canvas.create_image(1650, 50, image=self.bones_photo, tags="rect")
        self.bones_label = tk.Label(self.root, text=f"{self.total_bones}", font=("Comic Sans MS", 16), bg="#CCCCCC")
        self.bones_label.place(x=1700, y=30)

        self.update_map()

    def draw_grid(self):
        """Рисует сетку для движения."""
        for x in range(0, 1920, self.grid_size):
            self.map_canvas.create_line(x, 0, x, 1080, fill="lightgray")
        for y in range(0, 1080, self.grid_size):
            self.map_canvas.create_line(0, y, 1920, y, fill="lightgray")

    def generate_bones(self):
        """Генерация косточек на карте."""
        bones_count = min(self.max_bones_per_level,
                          10 * (2 ** (self.current_level - 1)))  # Ограничиваем количество косточек
        bones = set()  # Используем set для предотвращения дублирования косточек

        while len(bones) < bones_count:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) != tuple(self.dog_position):  # Исключаем начальную позицию собаки
                bones.add((x, y))  # Добавляем уникальную координату

        logging.info(f"Сгенерировано косточек: {bones}")
        return list(bones)  # Преобразуем в список для дальнейшей обработки

    def collect_bones(self):
        """Проверка и сбор косточек."""
        for bone in self.bones_positions[:]:
            if self.dog_position == [bone[0], bone[1]]:
                self.bones_positions.remove(bone)
                self.total_bones += 1

                # Сохраняем прогресс только при первом прохождении
                if not self.is_replay:
                    save_game_session(
                        user_id=self.user_id,
                        level=self.current_level,
                        score=self.total_bones,
                        duration=self.steps_taken,
                        steps=self.steps_taken,
                        health=100,
                        hunger=0,
                        sleepiness=0
                    )

                self.bones_label.config(text=f"{self.total_bones}")

        # Проверка на завершение уровня
        target_bones = 10 * (2 ** (self.current_level - 1))  # Целевое количество косточек
        if self.total_bones >= target_bones and not self.is_victory_screen_open:
            if not self.is_replay:
                self.show_victory_screen()
            else:
                self.start_game(is_replay=True)

        # Генерация новых косточек каждые 10 шагов
        if self.steps_taken % 10 == 0 and len(self.bones_positions) < self.max_bones_per_level:
            new_bones = self.generate_bones()
            for bone in new_bones:
                if bone not in self.bones_positions:
                    self.bones_positions.append(bone)  # Добавляем только уникальные косточки
            logging.info(f"Добавлены косточки: {new_bones}")

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
        """Обработчик для клавиши ESC."""
        if self.map_canvas:  # Проверяем, что игрок находится на карте
            if self.is_pause_menu_open:
                self.resume_game()  # Закрываем окно паузы и продолжаем игру
            else:
                self.show_pause_menu()  # Открываем окно паузы

    def show_pause_menu(self):
        """Создание окна паузы."""
        if self.is_pause_menu_open:
            return  # Если окно паузы уже открыто, ничего не делаем

        self.is_pause_menu_open = True  # Устанавливаем флаг

        self.pause_window = tk.Toplevel(self.root)
        self.pause_window.title("Пауза")
        self.pause_window.geometry("400x200")
        self.pause_window.configure(bg="#E5E5E5")
        self.pause_window.grab_set()  # Блокируем взаимодействие с основным окном

        # Кнопка "Сохранить и выйти"
        save_exit_button = tk.Button(
            self.pause_window,
            text="Сохранить и выйти",
            font=("Comic Sans MS", 16),
            bg="#FF6347",
            command=self.save_and_exit
        )
        save_exit_button.pack(pady=20)

        # Кнопка "Продолжить"
        continue_button = tk.Button(
            self.pause_window,
            text="Продолжить",
            font=("Comic Sans MS", 16),
            bg="#4CAF50",
            command=self.resume_game
        )
        continue_button.pack(pady=20)

    def resume_game(self):
        """Закрытие окна паузы и продолжение игры."""
        if self.is_pause_menu_open:
            self.pause_window.destroy()  # Закрываем окно паузы
            self.is_pause_menu_open = False  # Сбрасываем флаг
            self.is_game_active = True  # Возвращаем игру в активное состояние

    def save_and_exit(self):
        """Сохранение данных и выход в главное меню."""
        logging.info("Сохранение прогресса: уровень %d, собрано косточек %d.", self.current_level, self.total_bones)
        # Дополнительно можно добавить сохранение прогресса в базу данных.
        # Пример:
        # save_progress_to_database(user_id=self.user_id, level=self.current_level, bones=self.total_bones)
        self.return_to_main_menu_callback()  # Возврат в главное меню

    def update_map(self):
        """Обновление карты."""
        if self.is_victory_screen_open:  # Отключаем обновления, если окно победы открыто
            return

        self.map_canvas.delete("all")  # Удаляем старые объекты карты
        self.draw_grid()  # Перерисовываем сетку

        # Отображение косточек
        for x, y in self.bones_positions:
            self.map_canvas.create_image(
                x * self.grid_size + self.grid_size // 2,
                y * self.grid_size + self.grid_size // 2,
                image=self.bones_photo
            )

        # Отображение собаки
        if self.selected_dog:
            dog_image = Image.open(DOG_CHARACTERS[self.selected_dog]["image"]).resize(
                (self.grid_size, self.grid_size),
                Image.Resampling.LANCZOS
            )
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
        if self.total_bones >= target_bones and not self.is_victory_screen_open:
            self.show_victory_screen()

    def show_victory_screen(self):
        """Экран победы."""
        if self.is_victory_screen_open:
            return

        self.is_victory_screen_open = True
        self.is_game_active = False

        if not self.is_replay:
            # Сохранение прогресса при первом прохождении
            save_game_session(
                user_id=self.user_id,
                level=self.current_level,
                score=self.total_bones,
                duration=self.steps_taken,
                steps=self.steps_taken,
                health=100,
                hunger=0,
                sleepiness=0
            )
            self.completed_levels.add(self.current_level)
            self.max_unlocked_level = max(self.max_unlocked_level, self.current_level + 1)

        self.update_level_buttons()

        # Открываем окно победы
        victory_window = tk.Toplevel(self.root)
        victory_window.title("Уровень завершён!")
        victory_window.geometry("800x400")
        victory_window.configure(bg="#E5E5E5")
        victory_window.grab_set()

        # Текст победы
        victory_label = tk.Label(victory_window, text=f"Поздравляем! Уровень {self.current_level} завершён!",
                                 font=("Comic Sans MS", 24), bg="#E5E5E5")
        victory_label.place(x=200, y=20)  # Устанавливаем верхнюю позицию текста победы

        # Изображение собаки
        dog_image = Image.open(DOG_CHARACTERS[self.selected_dog]["image"]).resize((200, 200), Image.Resampling.LANCZOS)
        dog_photo = ImageTk.PhotoImage(dog_image)
        dog_label = tk.Label(victory_window, image=dog_photo, bg="#E5E5E5")
        dog_label.image = dog_photo
        dog_label.place(x=50, y=120)  # Сдвигаем изображение собаки вниз

        # Характеристики собаки
        dog_info = f"Порода: {self.selected_dog}"
        info_label = tk.Label(victory_window, text=dog_info, font=("Comic Sans MS", 16), bg="#E5E5E5")
        info_label.place(x=300, y=120)  # Размещаем характеристики собаки ниже текста победы и изображения собаки

        # Собрано косточек
        target_bones = 10 * (2 ** (self.current_level - 1))  # Геометрическая прогрессия
        collected_info = f"Собрано: {self.total_bones} из {target_bones}"
        score_label = tk.Label(victory_window, text=collected_info, font=("Comic Sans MS", 16), bg="#E5E5E5")
        score_label.place(x=300, y=170)  # Размещаем информацию о собранных косточках ниже характеристик собаки

        # Никнейм игрока
        user_info = get_user_by_id(self.user_id)
        username_label = tk.Label(victory_window, text=f"Никнейм: {user_info.username}", font=("Comic Sans MS", 16),
                                  bg="#E5E5E5")
        username_label.place(x=300, y=220)  # Размещаем никнейм игрока ниже собранных косточек

        # Кнопки управления
        button_frame = tk.Frame(victory_window, bg="#E5E5E5")
        button_frame.pack(side=tk.BOTTOM, pady=20)

        next_level_button = tk.Button(
            button_frame,
            text="Следующий уровень",
            font=("Comic Sans MS", 14),
            bg="#4CAF50",
            command=lambda: [victory_window.destroy(), self.start_next_level()]
        )
        next_level_button.pack(side=tk.LEFT, padx=10)

        """
        replay_button = tk.Button(
            button_frame,
            text="Пройти уровень снова",
            font=("Comic Sans MS", 14),
            bg="#FFEB3B",
            command=lambda: [victory_window.destroy(), self.start_game(is_replay=True)]  # Перезапуск уровня
        )
        replay_button.pack(side=tk.LEFT, padx=10)
        """

        exit_button = tk.Button(
            button_frame,
            text="Выйти в главное меню",
            font=("Comic Sans MS", 14),
            bg="#FF6347",
            command=lambda: [victory_window.destroy(), self.return_to_main_menu()]
        )
        exit_button.pack(side=tk.LEFT, padx=10)

    def close_victory_window(self):
        """Закрытие окна победы и сброс флага."""
        self.is_victory_screen_open = False
        self.is_game_active = True
        self.return_to_main_menu()  # Возвращаем в меню

    def return_to_main_menu(self):
        """Возврат в главное меню."""
        if self.is_pause_menu_open:
            self.pause_window.destroy()  # Закрываем окно паузы
            self.is_pause_menu_open = False  # Сбрасываем флаг

        clear_frame(self.root)  # Очищаем текущий экран
        self.show_main_menu()  # Переходим в главное меню

    def start_next_level(self):
        """Запуск следующего уровня."""
        self.current_level += 1  # Переход на следующий уровень
        self.total_bones = 0  # Сброс собранных косточек
        self.steps_taken = 0  # Сброс количества шагов
        self.dog_position = [1, 1]  # Возвращаем собаку в начальную позицию
        self.bones_positions = []  # Очищаем косточки
        self.is_victory_screen_open = False  # Закрываем экран победы, если он был открыт

        # Сохраняем новый прогресс в базу данных
        save_game_session(
            user_id=self.user_id,
            level=self.current_level,
            score=0,
            duration=0,
            steps=0,
            health=100,
            hunger=0,
            sleepiness=0
        )
        logging.info(f"Запуск уровня {self.current_level}.")
        self.countdown()  # Запускаем обратный отсчёт перед началом уровня

    def save_progress(self):
        """Сохранение игрового процесса в таблицу GameSessions."""
        if not self.user_id:
            logging.error("Ошибка: user_id равен None. Запись невозможна.")
            return

        try:
            # Рассчитываем длительность уровня и текущий счет
            duration = self.steps_taken
            score = self.total_bones

            # Логирование
            logging.info(
                f"Сохранение сессии: user_id={self.user_id}, level={self.current_level}, score={score}, duration={duration}")

            # Сохранение данных в базу
            save_game_session(
                user_id=self.user_id,
                level=self.current_level,
                score=self.total_bones,
                steps=self.steps_taken,  # Используйте количество шагов или время
                duration=self.steps_taken,  # Если 'steps' отражают время, используйте их
                health=100,  # Примерное значение
                hunger=0,  # Примерное значение
                sleepiness=0  # Примерное значение
            )

            logging.info("Прогресс успешно сохранен.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении прогресса: {e}")
            raise

    def create_main_menu_button(self):
        """Создаём кнопку для возврата в главное меню."""
        main_menu_button = tk.Button(
            self.root,
            text="Главное меню",
            font=("Comic Sans MS", 16),
            bg="lightgreen",
            command=self.show_main_menu,  # Вызов нового метода
        )
        main_menu_button.pack()

    def show_main_menu(self):
        """Переход в главное меню."""
        self.is_game_active = False  # Останавливаем игру, если мы возвращаемся в меню
        clear_frame(self.root)  # Очищаем текущий экран
        self.return_to_main_menu_callback()  # Вызов колбэка для возврата в главное меню