import tkinter as tk
from src.utils import clear_frame
from database.db_events import get_dogs, update_user_dog


def shop_ui(root, user_id):
    """Интерфейс магазина."""
    clear_frame(root)

    frame = tk.Frame(root, bg="#e5e5e5")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Магазин", font=("Comic Sans MS", 30), bg="#e5e5e5").pack(pady=20)

    dogs = get_dogs()  # Получить список собак из базы данных
    for dog in dogs:
        dog_frame = tk.Frame(frame, bg="#f8f8f8", bd=2, relief=tk.RIDGE)
        dog_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(dog_frame, text=dog.breed, font=("Comic Sans MS", 20), bg="#f8f8f8").pack(side=tk.LEFT, padx=10)
        tk.Button(dog_frame, text="Купить", command=lambda d=dog: update_user_dog(user_id, d.dog_id)).pack(
            side=tk.RIGHT, padx=10)

    tk.Button(frame, text="Назад", command=lambda: clear_frame(root), font=("Comic Sans MS", 20)).pack(pady=20)
