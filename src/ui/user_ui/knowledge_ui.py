import os
import tkinter as tk
from PIL import Image, ImageTk
from config import DOG_CHARACTERS, BASE_DIR
from src.utils import clear_frame
from database.info.Dogs_table import get_all_dogs


def knowledge_ui(root, user_app):
    """Интерфейс базы знаний о породах собак."""
    clear_frame(root)

    # Загружаем данные о породах собак из базы данных
    dog_data = get_all_dogs()
    if not dog_data:
        tk.Label(root, text="Не удалось загрузить данные о породах.", font=("Arial", 20)).pack()
        return

    index = {"current": 0}  # Индекс текущей породы

    def update_content():
        """Обновляет содержимое для текущей породы."""
        current_dog = dog_data[index["current"]]
        breed = current_dog.breed

        # Загружаем информацию из DOG_CHARACTERS
        dog_info = DOG_CHARACTERS.get(breed)
        if not dog_info:
            title_label.config(text="Нет данных о породе.")
            image_label.config(image=None)
            image_label.image = None
            characteristics_label.config(text="")
            behavior_label.config(text="")
            care_label.config(text="")
            admin_comments_label.config(text="")
            return

        # Загружаем изображение
        image_path = dog_info["image"]
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
        else:
            image_label.config(image=None)
            image_label.image = None

        # Обновляем текст
        title_label.config(text=breed)
        characteristics_label.config(text=f"Характеристики: {current_dog.characteristics}")
        behavior_label.config(text=f"Поведение: {current_dog.behavior}")
        care_label.config(text=f"Уход: {current_dog.care_info}")
        admin_comments_label.config(text=f"Комментарии: {current_dog.admin_comments}")

    def next_breed():
        """Переход к следующей породе."""
        index["current"] = (index["current"] + 1) % len(dog_data)
        update_content()

    def previous_breed():
        """Переход к предыдущей породе."""
        index["current"] = (index["current"] - 1) % len(dog_data)
        update_content()

    # Основной интерфейс
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="", font=("Arial", 20), bg="#f0f0f0")
    title_label.pack(pady=10)

    image_label = tk.Label(frame, bg="#f0f0f0")
    image_label.pack(pady=10)

    characteristics_label = tk.Label(frame, text="", font=("Arial", 14), bg="#f0f0f0", wraplength=600)
    characteristics_label.pack(pady=5)

    behavior_label = tk.Label(frame, text="", font=("Arial", 14), bg="#f0f0f0", wraplength=600)
    behavior_label.pack(pady=5)

    care_label = tk.Label(frame, text="", font=("Arial", 14), bg="#f0f0f0", wraplength=600)
    care_label.pack(pady=5)

    admin_comments_label = tk.Label(frame, text="", font=("Arial", 14), bg="#f0f0f0", wraplength=600)
    admin_comments_label.pack(pady=5)

    # Кнопки навигации
    btn_frame = tk.Frame(frame, bg="#f0f0f0")
    btn_frame.pack(pady=20)

    back_button = tk.Button(
        btn_frame,
        text="Назад",
        font=("Arial", 14),
        command=lambda: [clear_frame(root), user_app.show_user_dashboard()]
    )
    back_button.pack(side=tk.LEFT, padx=5)

    prev_button = tk.Button(btn_frame, text="Предыдущая", font=("Arial", 14), command=previous_breed)
    prev_button.pack(side=tk.LEFT, padx=5)

    next_button = tk.Button(btn_frame, text="Следующая", font=("Arial", 14), command=next_breed)
    next_button.pack(side=tk.LEFT, padx=5)

    update_content()  # Инициализация первого отображения
