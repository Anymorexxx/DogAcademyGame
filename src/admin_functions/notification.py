from tkinter import messagebox

class Notification:
    def __init__(self, root):
        self.root = root

    def show_info(self, title, message):
        """Отображение информационного уведомления"""
        messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        """Отображение предупреждения"""
        messagebox.showwarning(title, message)

    def show_error(self, title, message):
        """Отображение ошибки"""
        messagebox.showerror(title, message)

    def show_notification(self, title, message):
        """Отображение общего уведомления"""
        self.show_info(title, message)
