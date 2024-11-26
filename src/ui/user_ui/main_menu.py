import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import math

from config import EXIT_BUTTON_WIDTH, EXIT_BUTTON_HEIGHT, BUTTON_COLOR_EXIT
from src.ui.user_ui.game_ui import GameUI
from src.ui.user_ui.profile_ui import profile_ui
from src.ui.user_ui.shop_ui import shop_ui
from src.ui.user_ui.knowledge_ui import knowledge_ui
from src.utils import clear_frame

# Пути к изображениям собак
DOG_IMAGES = [
    "F:/Projects/Dog_Academy/assets/dogs/Chihuahua.png",
    "F:/Projects/Dog_Academy/assets/dogs/Corgi.png",
    "F:/Projects/Dog_Academy/assets/dogs/Golden_Retriever.png",
    "F:/Projects/Dog_Academy/assets/dogs/Husky.png",
    "F:/Projects/Dog_Academy/assets/dogs/Pomeranian.png",
    "F:/Projects/Dog_Academy/assets/dogs/Pug.png",
    "F:/Projects/Dog_Academy/assets/dogs/Yorkshire_Terrier.png"
]

# Настройки
BACKGROUND_COLOR = "#E5E5E5"  # Цвет фона
BUTTON_COLOR_PLAY = "#4CAF50"  # Цвет кнопки играть
BUTTON_TEXT_COLOR = "white"  # Цвет текста на кнопке
FONT = ("Arial", 12)
BIG_FONT = ("Arial", 24)
PLAY_BUTTON_RADIUS = 100  # Радиус кнопки "Играть"


class UserApp:
    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.geometry("1920x1080")
        self.root.title("Собачья академия")
        self.show_user_dashboard()

    def show_user_dashboard(self):
        """Показать интерфейс пользователя."""
        center_x, center_y = 960, 540  # Центр экрана
        radius = 300  # Радиус круга для размещения собак
        num_dogs = len(DOG_IMAGES)

        # Верхняя панель
        top_panel = tk.Frame(self.root, bg="#333333", height=100)
        top_panel.pack(fill=tk.X, side=tk.TOP)

        # Кнопки на верхней панели
        profile_button = tk.Button(
            top_panel,
            text="Профиль",
            bg="#555555",
            fg="white",
            font=FONT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.show_profile
        )
        profile_button.pack(side=tk.LEFT, padx=20)

        shop_button = tk.Button(
            top_panel,
            text="Магазин",
            bg="#555555",
            fg="white",
            font=FONT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.show_shop
        )
        shop_button.pack(side=tk.LEFT, padx=20)

        knowledge_button = tk.Button(
            top_panel,
            text="База знаний",
            bg="#555555",
            fg="white",
            font=FONT,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.show_knowledge
        )
        knowledge_button.pack(side=tk.LEFT, padx=20)

        # Размещение собак по кругу
        self.place_dog_images(center_x, center_y, radius, num_dogs)

        # Кнопка "Играть" (увеличенная)
        play_button_canvas = tk.Canvas(
            self.root,
            width=PLAY_BUTTON_RADIUS * 2,
            height=PLAY_BUTTON_RADIUS * 2,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        play_button_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        play_button_canvas.create_oval(
            0, 0, PLAY_BUTTON_RADIUS * 2, PLAY_BUTTON_RADIUS * 2,
            fill=BUTTON_COLOR_PLAY,
            outline=BUTTON_COLOR_PLAY,
        )
        play_button_canvas.create_text(
            PLAY_BUTTON_RADIUS,
            PLAY_BUTTON_RADIUS,
            text="Играть",
            fill=BUTTON_TEXT_COLOR,
            font=BIG_FONT,
        )
        play_button_canvas.tag_bind("all", "<Button-1>", lambda e: self.play_game())

    def place_dog_images(self, center_x, center_y, radius, num_dogs):
        """Размещает изображения собак по кругу."""
        angle_step = 2 * math.pi / num_dogs  # Шаг угла для размещения собак
        for i in range(num_dogs):
            angle = i * angle_step
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            # Загрузка изображения собаки
            image_path = DOG_IMAGES[i]
            try:
                dog_image = Image.open(image_path)
                dog_image = dog_image.resize((100, 100), Image.Resampling.LANCZOS)
                dog_photo = ImageTk.PhotoImage(dog_image)

                # Создание метки с изображением
                dog_label = tk.Label(self.root, image=dog_photo, bg=BACKGROUND_COLOR)
                dog_label.image = dog_photo  # Сохраняем ссылку на изображение
                dog_label.place(x=x - 50, y=y - 50)  # Центрируем метку относительно позиции
            except Exception as e:
                print(f"Ошибка загрузки изображения {image_path}: {e}")

    def show_profile(self):
        """Показать экран профиля пользователя."""
        self.clear_frame()
        profile_ui(self.root, self.user_id)  # Передаем user_id в profile_ui

    def show_shop(self):
        """Показать экран магазина."""
        self.clear_frame()
        shop_ui(self.root)

    def show_knowledge(self):
        """Показать базу знаний."""
        self.clear_frame()
        knowledge_ui(self.root)

    def clear_frame(self):
        """Очистить текущий экран."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def play_game(self):
        """Переход к игровому интерфейсу."""
        clear_frame(self.root)  # Очищаем главное меню
        GameUI(self.root, self.user_id)  # Открываем игровой интерфейс
        print("Запуск игры...")

    def exit_app(self):
        """Заглушка для выхода."""
        print("Приложение закрыто")
        self.root.quit()

# Запуск главного окна
if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root, user_id=123)  # Передаем user_id (это может быть получено после авторизации)
    root.mainloop()

