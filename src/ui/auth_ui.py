import tkinter as tk
from tkinter import messagebox
from config import BACKGROUND_COLOR, PRIMARY_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, FONT, BIG_FONT, ADMIN_LOGIN, ADMIN_PASSWORD
from src.ui.admin_ui import AdminApp  # Импорт интерфейса администратора
from database.db_events import create_user, check_user
from src.ui.user_ui.main_menu import UserApp

class DogAcademyApp:
    def __init__(self, root):
        self.root = root
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
        """Показать главное меню с названием игры и кнопками."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        # Название игры
        title = tk.Label(
            self.current_frame,
            text="Dog Academy Game",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=BIG_FONT,
        )
        title.pack(pady=50)

        # Кнопка "Войти"
        login_button = tk.Button(
            self.current_frame,
            text="Войти",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.show_login_screen,
        )
        login_button.pack(pady=20)

        # Кнопка "Зарегистрироваться"
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

        # Заголовок
        title = tk.Label(
            self.current_frame,
            text="Авторизация",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=BIG_FONT,
        )
        title.pack(pady=50)

        # Логин
        login_label = tk.Label(self.current_frame, text="Логин:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        login_label.pack()
        self.login_entry = tk.Entry(self.current_frame, font=FONT)
        self.login_entry.pack(pady=10)

        # Пароль
        password_label = tk.Label(self.current_frame, text="Пароль:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        password_label.pack()
        self.password_entry = tk.Entry(self.current_frame, show="*", font=FONT)
        self.password_entry.pack(pady=10)

        # Кнопка "Показать пароль"
        show_password_button = tk.Button(
            self.current_frame,
            text="Показать пароль",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.toggle_password,
        )
        show_password_button.pack(pady=10)

        # Кнопка "Войти"
        login_button = tk.Button(
            self.current_frame,
            text="Войти",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.login_user,
        )
        login_button.pack(pady=20)

        # Кнопка "Вернуться на главную"
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
            self.show_admin_panel()  # Переходим к админ-панели
        elif check_user(login, password):
            messagebox.showinfo("Успех", "Вы успешно авторизованы!")
            self.show_user_dashboard()  # Переходим к панели пользователя
        else:
            messagebox.showerror("Ошибка", "Неверные данные. Попробуйте снова.")

    def show_admin_panel(self):
        """Отображение интерфейса администратора."""
        self.clear_frame()
        AdminApp(self.root)  # Создаем экземпляр админ-панели

    def show_registration_screen(self):
        """Показать экран регистрации."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.current_frame.pack(expand=True)

        # Заголовок
        title = tk.Label(
            self.current_frame,
            text="Регистрация",
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_COLOR,
            font=BIG_FONT,
        )
        title.pack(pady=50)

        # Логин
        login_label = tk.Label(self.current_frame, text="Логин:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        login_label.pack()
        self.reg_login_entry = tk.Entry(self.current_frame, font=FONT)
        self.reg_login_entry.pack(pady=10)

        # Пароль
        password_label = tk.Label(self.current_frame, text="Пароль:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        password_label.pack()
        self.reg_password_entry = tk.Entry(self.current_frame, show="*", font=FONT)
        self.reg_password_entry.pack(pady=10)

        # Никнейм
        username_label = tk.Label(self.current_frame, text="Никнейм:", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, font=FONT)
        username_label.pack()
        self.username_entry = tk.Entry(self.current_frame, font=FONT)
        self.username_entry.pack(pady=10)

        # Кнопка "Зарегистрироваться"
        register_button = tk.Button(
            self.current_frame,
            text="Зарегистрироваться",
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=FONT,
            command=self.register_user,
        )
        register_button.pack(pady=20)

        # Кнопка "Вернуться на главную"
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
        username = self.username_entry.get()  # Получаем имя пользователя

        if login and password and username:
            success, message = create_user(login, password, username)  # Передаем имя пользователя
            if success:
                messagebox.showinfo("Успех", message)
                self.show_login_screen()
            else:
                messagebox.showerror("Ошибка", message)
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")

    def show_user_dashboard(self):
        self.clear_frame()
        """Перейти к главному меню пользователя после авторизации."""
        UserApp(self.root)
