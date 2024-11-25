import tkinter as tk
from datetime import datetime

class Notification:
    def __init__(self, parent, message, timestamp):
        self.frame = tk.Frame(parent, bg="#2f2b38", pady=5)
        self.frame.pack(fill="x", pady=5)

        self.message_label = tk.Label(self.frame, text=message, bg="#2f2b38", fg="#b2acc0", font=("Comic Sans MS", 12))
        self.message_label.pack(side="left", padx=10)

        self.timestamp_label = tk.Label(self.frame, text=self.format_timestamp(timestamp), bg="#2f2b38", fg="#b2acc0", font=("Comic Sans MS", 10))
        self.timestamp_label.pack(side="right", padx=10)

    def format_timestamp(self, timestamp):
        """Форматирование метки времени."""
        return datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M:%S")
