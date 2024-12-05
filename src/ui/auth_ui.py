import tkinter as tk
from tkinter import messagebox
from config import BACKGROUND_COLOR, PRIMARY_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, FONT, BIG_FONT, ADMIN_LOGIN, ADMIN_PASSWORD
from src.auth import login_user
from src.ui.admin_ui import AdminApp  # Импорт интерфейса администратора
from database.db_events import create_user
from src.ui.user_ui.main_menu import UserApp

class DogAcademyApp:
    def __init__(self, root, user_id=None):
        """Инициализация приложения."""
        self.root = root
        self.user_id = user_id
        self.root.title("Dog Academy Game")
        self.root.geometry("1920x1080")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.current_frame = None
        self.show_main_menu()

    def clear_frame(self):
        """Очистить текущий фрейм."""
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        """Показать главное меню."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        title = tk.Label(
            self.current_frame,
            text="Dog Academy Game",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=BIG_FONT,
        )
        title.pack(pady=50)

        login_button = tk.Button(
            self.current_frame,
            text="Войти",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.show_login_screen,
        )
        login_button.pack(pady=20)

        register_button = tk.Button(
            self.current_frame,
            text="Зарегистрироваться",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.show_registration_screen,
        )
        register_button.pack(pady=20)

    def show_login_screen(self):
        """Показать экран авторизации."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        title = tk.Label(
            self.current_frame,
            text="Авторизация",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=BIG_FONT,
        )
        title.pack(pady=50)

        login_label = tk.Label(self.current_frame, text="Логин:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        login_label.pack()
        self.login_entry = tk.Entry(self.current_frame, font=FONT)
        self.login_entry.pack(pady=10)

        password_label = tk.Label(self.current_frame, text="Пароль:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        password_label.pack()
        self.password_entry = tk.Entry(self.current_frame, show="*", font=FONT)
        self.password_entry.pack(pady=10)

        show_password_button = tk.Button(
            self.current_frame,
            text="Показать пароль",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.toggle_password,
        )
        show_password_button.pack(pady=10)

        login_button = tk.Button(
            self.current_frame,
            text="Войти",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.login_user,
        )
        login_button.pack(pady=20)

        back_button = tk.Button(
            self.current_frame,
            text="Вернуться на главную",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.show_main_menu,
        )
        back_button.pack(pady=20)

    def toggle_password(self):
        """Переключение видимости пароля."""
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def login_user(self):
        """Проверка данных для авторизации."""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            messagebox.showinfo("Успех", "Вы успешно авторизованы как администратор!")
            self.user_id = None  # Администратору не нужен user_id
            self.show_admin_panel()
        else:
            success, user_id = login_user(login, password)
            if success:
                messagebox.showinfo("Успех", "Вы успешно авторизованы!")
                self.user_id = user_id  # Сохраняем user_id
                self.show_user_dashboard()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def show_admin_panel(self):
        """Отображение интерфейса администратора."""
        self.clear_frame()
        AdminApp(self.root)

    def show_registration_screen(self):
        """Показать экран регистрации."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        title = tk.Label(
            self.current_frame,
            text="Регистрация",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=BIG_FONT,
        )
        title.pack(pady=50)

        login_label = tk.Label(self.current_frame, text="Логин:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        login_label.pack()
        self.reg_login_entry = tk.Entry(self.current_frame, font=FONT)
        self.reg_login_entry.pack(pady=10)

        password_label = tk.Label(self.current_frame, text="Пароль:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        password_label.pack()
        self.reg_password_entry = tk.Entry(self.current_frame, show="*", font=FONT)
        self.reg_password_entry.pack(pady=10)

        username_label = tk.Label(self.current_frame, text="Никнейм:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        username_label.pack()
        self.username_entry = tk.Entry(self.current_frame, font=FONT)
        self.username_entry.pack(pady=10)

        register_button = tk.Button(
            self.current_frame,
            text="Зарегистрироваться",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.register_user,
        )
        register_button.pack(pady=20)

        back_button = tk.Button(
            self.current_frame,
            text="Вернуться на главную",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.show_main_menu,
        )
        back_button.pack(pady=20)

    def toggle_registration_password(self):
        """Переключение видимости пароля для регистрации."""
        if self.reg_password_entry.cget('show') == '*':
            self.reg_password_entry.config(show='')
        else:
            self.reg_password_entry.config(show='*')

    def register_user(self):
        """Регистрация нового пользователя."""
        login = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        username = self.username_entry.get()

        if login and password and username:
            success, message = create_user(login, password, username)
            if success:
                messagebox.showinfo("Успех", message)
                self.show_login_screen()
            else:
                messagebox.showerror("Ошибка", message)
        else:
            messagebox.showerror("Ошибка", "Заполните все поля.")

    def show_user_dashboard(self):
        """Переход к пользовательскому интерфейсу."""
        self.clear_frame()
        UserApp(self.root, self.user_id)
