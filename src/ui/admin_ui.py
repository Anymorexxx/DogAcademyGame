import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from sqlalchemy.exc import SQLAlchemyError

from config import SETTINGS_IMG
from database.db_session import get_session
from database.models import Dogs, Questions, Users
from src.admin_functions import admin_logging, statistics
from src.utils import clear_frame, feature_in_development_admin  # Импортируем общую функцию для очистки фрейма
from database.db_events import check_user, get_all_users, get_all_questions, get_all_dogs, delete_dog, update_dog_info, \
    add_question_to_db, add_user_to_db, add_dog_to_db, delete_question, delete_user

# Конфигурация цветов из config.py
BACKGROUND_COLOR = "#403d49"
TOP_BAR_COLOR = "#383441"
TEXT_COLOR = "#b2acc0"
BUTTON_COLOR = "#403d49"
MENU_COLOR = "#2f2b38"
MENU_OPACITY = 0.9  # Прозрачность меню

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Админ-Панель")
        self.root.geometry("1920x1080")
        self.root.config(bg=BACKGROUND_COLOR)

        # Верхняя панель
        self.top_bar = tk.Frame(self.root, bg=TOP_BAR_COLOR, height=60)
        self.top_bar.pack(side="top", fill="x")

        # Кнопка настроек
        settings_img = Image.open(SETTINGS_IMG)
        settings_img = settings_img.resize((40, 40), Image.Resampling.LANCZOS)
        settings_icon = ImageTk.PhotoImage(settings_img)

        self.settings_button = tk.Button(
            self.top_bar,
            image=settings_icon,
            bg=TOP_BAR_COLOR,
            activebackground=TOP_BAR_COLOR,
            bd=0
        )
        self.settings_button.image = settings_icon  # Сохраняем ссылку на изображение
        self.settings_button.pack(side="left", padx=10, pady=10)

        # Кнопки навигации
        self.create_nav_button("Логирование", lambda: admin_logging.show_logs(self.main_frame))
        self.create_nav_button("Статистика", lambda: statistics.show_statistics(self.main_frame))
        self.create_nav_button("Уведомления", lambda: self.show_notifications(self.main_frame))
        self.create_nav_button("Безопасность", lambda: self.show_security(self.main_frame))
        self.create_nav_button("Открыть сессию пользователя", self.open_user_session)

        # Бургер-меню
        self.menu_button = tk.Button(
            self.top_bar,
            text="☰ Меню",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 14),
            activebackground=BUTTON_COLOR,
            activeforeground=TEXT_COLOR,
            bd=0,
            command=self.toggle_menu
        )
        self.menu_button.pack(side="right", padx=10, pady=10)

        # Основное окно
        self.main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        # Бургер-меню (скрытое по умолчанию)
        self.menu_frame = tk.Frame(self.root, bg=MENU_COLOR, width=300)
        self.menu_frame.place(x=1620, y=60, width=300, height=1020)
        self.menu_frame.lower()
        self.menu_visible = False

    def toggle_menu(self):
        """Показ или скрытие меню."""
        if self.menu_visible:
            self.menu_frame.lower()
            self.menu_visible = False
        else:
            self.menu_frame.lift()
            self.menu_visible = True
            self.populate_menu()

    def populate_menu(self):
        # Очистка меню
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Список разделов и их элементов
        menu_sections = [
            ("Работа с базой данных", [
                ("Редактирование пользователей", self.manage_users),
                ("Управление вопросами", self.manage_questions),
                ("Управление собаками", self.manage_dogs),
                ("Просмотр таблиц", self.view_tables),
            ]),
            ("Управление игровым контентом", [
                ("Создание и настройка уровней", lambda: feature_in_development_admin(self.main_frame)),
                ("Настройка параметров собаки", lambda: feature_in_development_admin(self.main_frame)),
            ]),
            ("Управление интерфейсом пользователя", [
                ("Добавление подсказок в интерфейс", lambda: feature_in_development_admin(self.main_frame)),
            ])
        ]

        # Определяем максимальную ширину текста для настройки ширины меню и кнопок
        max_text_length = max(
            len(title) for title, items in menu_sections
        ) + max(
            max(len(text) for text, _ in items) for _, items in menu_sections
        )
        menu_width = max(300, max_text_length * 10)  # Устанавливаем минимальную ширину

        # Обновляем ширину меню
        self.menu_frame.config(width=menu_width)

        # Высота одной кнопки и отступов
        button_height = 40
        button_spacing = 10
        section_spacing = 15

        total_height = 0

        for title, items in menu_sections:
            section_label = tk.Label(
                self.menu_frame,
                text=title,
                bg=MENU_COLOR,
                fg=TEXT_COLOR,
                font=("Comic Sans MS", 14, "bold"),
            )
            section_label.pack(fill="x", padx=10, pady=5)

            for text, command in items:
                item_button = tk.Button(
                    self.menu_frame,
                    text=text,
                    bg=BUTTON_COLOR,
                    fg=TEXT_COLOR,
                    font=("Comic Sans MS", 12),
                    activebackground=BUTTON_COLOR,
                    activeforeground=TEXT_COLOR,
                    bd=0,
                    command=command  # Используем lambda, чтобы передать команду без аргументов
                )
                item_button.pack(fill="x", padx=20, pady=5)

        # Кнопка "Выйти" внизу меню
        exit_button = tk.Button(
            self.menu_frame,
            text="Выйти",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 12),
            activebackground=BUTTON_COLOR,
            activeforeground=TEXT_COLOR,
            bd=0,
            command=self.exit_app
        )
        exit_button.pack(side="bottom", padx=10, pady=20)  # Размещение внизу

    def create_nav_button(self, text, command):
        """Создание кнопки навигации."""
        button = tk.Button(
            self.top_bar,
            text=text,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 14),
            activebackground=BUTTON_COLOR,
            activeforeground=TEXT_COLOR,
            bd=0,
            padx=10,
            pady=5,
            command=command  # Передаем функцию напрямую
        )
        button.pack(side="left", padx=10, pady=10)

    def open_manage_dogs_window(self, frame):
        """Открыть окно для управления собаками."""
        self.manage_dogs()

    def manage_ui_tips(self, frame):
        # Пример логики для управления подсказками
        print("Управление подсказками интерфейса.")
        # Код для управления подсказками (например, скрытие или показ подсказок)
        tk.Label(frame, text="Здесь будут подсказки для интерфейса", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Comic Sans MS", 16)).pack()

    def show_notifications(self, frame):
        """Отображение экрана уведомлений"""
        clear_frame(frame)  # Очищаем текущий экран
        tk.Label(
            frame,
            text="Модуль <Уведомления> в разработке.\nВ планах реализовать: создание оповещений для пользователей (обновления, новости), сообщения от БД (корректность работы)",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 16)
        ).pack(expand=True)

    def show_security(self, frame):
        """Отображение экрана безопасности"""
        clear_frame(frame)  # Очищаем текущий экран
        tk.Label(
            frame,
            text="Модуль <Безопасность> в разработке.\nВ планах реализовать: управление доступом (создание других админов, смена пароля администратора).",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 16)
        ).pack(expand=True)

    def change_ui_settings(self, frame):
        clear_frame(frame)
        """Метод для изменения цветовой схемы, фона и логотипа"""
        print("Изменение UI настроек")  # Пока просто тестовый вывод

    def exit_app(self):
        """Закрыть приложение."""
        self.root.quit()

    # Метод для авторизации под пользователем
    def open_user_session(self):
        """Открыть новую сессию пользователя."""
        user_login_window = tk.Toplevel(self.root)
        user_login_window.title("Авторизация пользователя")
        user_login_window.geometry("400x300")
        user_login_window.configure(bg=BACKGROUND_COLOR)

        tk.Label(
            user_login_window,
            text="Введите логин пользователя:",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 12)
        ).pack(pady=20)

        user_login_entry = tk.Entry(user_login_window, font=("Comic Sans MS", 12))
        user_login_entry.pack(pady=10)

        def open_user_interface():
            login = user_login_entry.get()  # Получаем логин из поля ввода
            user_id = check_user(login)  # Передаем логин для проверки

            if user_id:
                user_login_window.destroy()
                user_window = tk.Toplevel(self.root)
                from src.ui.user_ui.main_menu import UserApp
                UserApp(user_window, user_id=user_id)
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден.")

        tk.Button(
            user_login_window,
            text="Открыть сессию",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 12),
            command=open_user_interface
        ).pack(pady=20)

        tk.Button(
            user_login_window,
            text="Отмена",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Comic Sans MS", 12),
            command=user_login_window.destroy
        ).pack(pady=10)

    def manage_users(self):
        """Управление пользователями."""
        clear_frame(self.main_frame)

        tk.Label(self.main_frame, text="Управление пользователями", font=("Comic Sans MS", 16), bg=BACKGROUND_COLOR,
                 fg=TEXT_COLOR).pack()

        # Кнопка добавления нового пользователя
        tk.Button(
            self.main_frame,
            text="Добавить пользователя",
            command=self.open_add_user_window,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # Кнопка обновления списка
        tk.Button(
            self.main_frame,
            text="Обновить список",
            command=self.manage_users,  # Перезагрузка данных
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        users = get_all_users()  # Получение списка пользователей

        if not users:
            tk.Label(self.main_frame, text="Нет пользователей в базе данных.", bg=BACKGROUND_COLOR,
                     fg=TEXT_COLOR).pack()
            return

        # Отображение данных в таблице
        table = ttk.Treeview(self.main_frame, columns=("ID", "Логин", "Имя пользователя", "Уровень"), show="headings")
        table.heading("ID", text="ID")
        table.heading("Логин", text="Логин")
        table.heading("Имя пользователя", text="Имя пользователя")
        table.heading("Уровень", text="Уровень")
        table.pack(fill="both", expand=True, pady=10)

        # Очистка старых записей из таблицы
        for row in table.get_children():
            table.delete(row)

        # Добавление данных из базы
        for user in users:
            table.insert("", "end", values=(user.user_id, user.auth.login, user.username, user.level))

        def delete_selected():
            selected_item = table.selection()
            if not selected_item:
                messagebox.showwarning("Удаление", "Выберите пользователя для удаления.")
                return
            user_id = table.item(selected_item, "values")[0]
            success, message = delete_user(user_id)
            if success:
                messagebox.showinfo("Успех", message)
                self.manage_users()  # Обновление списка
            else:
                messagebox.showerror("Ошибка", message)

        # Кнопка удаления
        tk.Button(
            self.main_frame,
            text="Удалить выбранного пользователя",
            command=delete_selected,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

    def manage_questions(self):
        """Управление вопросами."""
        clear_frame(self.main_frame)

        tk.Label(self.main_frame, text="Управление вопросами", font=("Comic Sans MS", 16), bg=BACKGROUND_COLOR,
                 fg=TEXT_COLOR).pack()

        # Кнопка добавления нового вопроса
        tk.Button(
            self.main_frame,
            text="Добавить вопрос",
            command=self.open_add_question_window,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # Кнопка обновления списка
        tk.Button(
            self.main_frame,
            text="Обновить список",
            command=self.manage_questions,  # Перезагрузка данных
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        questions = get_all_questions()  # Получение списка вопросов

        if not questions:
            tk.Label(self.main_frame, text="Нет вопросов в базе данных.", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
            return

        # Отображение данных в таблице
        table = ttk.Treeview(self.main_frame, columns=("ID", "Вопрос", "Полезная информация"), show="headings")
        table.heading("ID", text="ID")
        table.heading("Вопрос", text="Вопрос")
        table.heading("Полезная информация", text="Полезная информация")
        table.pack(fill="both", expand=True, pady=10)

        # Очистка таблицы перед заполнением новыми данными
        for row in table.get_children():
            table.delete(row)

        for question in questions:
            table.insert("", "end", values=(question.question_id, question.question_text, question.helpful_info))

        def delete_selected():
            selected_item = table.selection()
            if not selected_item:
                messagebox.showwarning("Удаление", "Выберите вопрос для удаления.")
                return

            question_id = table.item(selected_item, "values")[0]  # Получение ID вопроса
            success, message = delete_question(question_id)  # Вызов метода для удаления вопроса
            if success:
                messagebox.showinfo("Успех", message)
                self.manage_questions()  # Обновление списка вопросов
            else:
                messagebox.showerror("Ошибка", message)

        # Кнопка удаления
        tk.Button(
            self.main_frame,
            text="Удалить выбранный вопрос",
            command=delete_selected,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

    def manage_dogs(self):
        """Управление породами собак."""
        clear_frame(self.main_frame)

        # Заголовок
        tk.Label(self.main_frame, text="Управление породами собак", font=("Comic Sans MS", 16), bg=BACKGROUND_COLOR,
                 fg=TEXT_COLOR).pack()

        # Функция удаления выбранной породы
        def delete_selected():
            selected_item = table.selection()
            if not selected_item:
                messagebox.showwarning("Удаление", "Выберите породу для удаления.")
                return
            dog_id = table.item(selected_item, "values")[0]  # ID породы
            success, message = delete_dog(dog_id)
            if success:
                messagebox.showinfo("Успех", message)
                self.manage_dogs()  # Обновление списка
            else:
                messagebox.showerror("Ошибка", message)

        # Функция редактирования выбранной породы
        def edit_selected():
            selected_item = table.selection()
            if not selected_item:
                messagebox.showwarning("Редактирование", "Выберите породу для редактирования.")
                return

            # Получение данных выбранной породы
            dog_data = table.item(selected_item, "values")

            # Пример dog_data: ('dog_id', 'breed', 'characteristics', 'behavior', 'care_info', 'admin_comments')

            if len(dog_data) < 6:
                messagebox.showwarning("Ошибка", "Недостаточно данных для редактирования.")
                return

            dog_id = dog_data[0]
            breed = dog_data[1]
            characteristics = dog_data[2]
            behavior = dog_data[3]
            care_info = dog_data[4]  # Дополнительная информация о породе
            admin_comments = dog_data[5]  # Комментарии администратора

            # Вызов функции открытия окна редактирования породы, передавая все необходимые данные
            self.open_edit_dog_window(dog_id, breed, characteristics, behavior, care_info, admin_comments)

        # Кнопка добавления новой породы
        tk.Button(
            self.main_frame,
            text="Добавить породу",
            command=self.open_add_dog_window,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # Кнопка обновления списка
        tk.Button(
            self.main_frame,
            text="Обновить список",
            command=self.manage_dogs,  # Повторный вызов для обновления данных
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # Кнопка удаления
        tk.Button(
            self.main_frame,
            text="Удалить выбранную породу",
            command=delete_selected,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # Кнопка редактирования
        tk.Button(
            self.main_frame,
            text="Редактировать выбранную породу",
            command=edit_selected,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # Получение данных из базы
        dogs = get_all_dogs()

        if not dogs:
            tk.Label(self.main_frame, text="Нет записей о породах в базе данных.", bg=BACKGROUND_COLOR,
                     fg=TEXT_COLOR).pack()
            return

        # Создание таблицы
        table = ttk.Treeview(self.main_frame, columns=(
        "ID", "Порода", "Характеристики", "Поведение", "Информация по уходу", "Комментарии"), show="headings")
        table.heading("ID", text="ID")
        table.heading("Порода", text="Порода")
        table.heading("Характеристики", text="Характеристики")
        table.heading("Поведение", text="Поведение")
        table.heading("Информация по уходу", text="Информация по уходу")
        table.heading("Комментарии", text="Комментарии")
        table.pack(fill="both", expand=True, pady=10)

        # Заполнение таблицы данными о породах
        for dog in dogs:
            table.insert("", "end", values=(
            dog.dog_id, dog.breed, dog.characteristics, dog.behavior, dog.care_info, dog.admin_comments))

    def open_edit_dog_window(self, dog_id, breed, characteristics, behavior, care_info, admin_comments):
        """Открыть окно редактирования данных о породе собак."""
        edit_dog_window = tk.Toplevel(self.root)
        edit_dog_window.title("Редактировать данные породы")
        edit_dog_window.geometry("500x400")
        edit_dog_window.configure(bg=BACKGROUND_COLOR)

        fields = {
            "Порода": (breed, tk.Entry(edit_dog_window, font=("Comic Sans MS", 12))),
            "Характеристики": (characteristics, tk.Entry(edit_dog_window, font=("Comic Sans MS", 12))),
            "Поведение": (behavior, tk.Entry(edit_dog_window, font=("Comic Sans MS", 12))),
            "Уход": (care_info, tk.Entry(edit_dog_window, font=("Comic Sans MS", 12))),
            "Комментарии администратора": (admin_comments, tk.Entry(edit_dog_window, font=("Comic Sans MS", 12))),
        }

        for idx, (label_text, (value, entry)) in enumerate(fields.items()):
            tk.Label(edit_dog_window, text=label_text, bg=BACKGROUND_COLOR, fg=TEXT_COLOR,
                     font=("Comic Sans MS", 12)).grid(row=idx, column=0, pady=10, padx=10)
            entry.insert(0, value)
            entry.grid(row=idx, column=1, pady=10, padx=10)

        def save_changes():
            updated_data = {key: entry.get() for key, (_, entry) in fields.items()}
            success, message = update_dog_info(dog_id, updated_data["Порода"], updated_data["Характеристики"])
            if success:
                messagebox.showinfo("Успех", message)
                edit_dog_window.destroy()
                self.manage_dogs()  # Обновление списка пород
            else:
                messagebox.showerror("Ошибка", message)

        tk.Button(edit_dog_window, text="Сохранить", command=save_changes, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(
            row=len(fields), column=0, pady=20)
        tk.Button(edit_dog_window, text="Отмена", command=edit_dog_window.destroy, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(
            row=len(fields), column=1, pady=20)

    def view_tables(self):
        """Просмотр всех таблиц."""
        clear_frame(self.main_frame)

        tk.Label(self.main_frame, text="Просмотр всех таблиц", font=("Comic Sans MS", 16), bg=BACKGROUND_COLOR,
                 fg=TEXT_COLOR).pack()

        # Создаём вкладки для отображения таблиц
        tab_control = ttk.Notebook(self.main_frame)

        # Таблица пользователей
        users_frame = ttk.Frame(tab_control)
        tab_control.add(users_frame, text="Пользователи")
        users_data = get_all_users()
        if users_data:
            self.create_table_view(users_frame, users_data, ["user_id", "login", "username", "level"])
        else:
            tk.Label(users_frame, text="Нет данных о пользователях.", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()

        # Таблица собак
        dogs_frame = ttk.Frame(tab_control)
        tab_control.add(dogs_frame, text="Породы собак")
        dogs_data = get_all_dogs()
        if dogs_data:
            self.create_table_view(dogs_frame, dogs_data, ["dog_id", "breed", "characteristics", "behavior"])
        else:
            tk.Label(dogs_frame, text="Нет данных о породах собак.", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()

        # Таблица вопросов
        questions_frame = ttk.Frame(tab_control)
        tab_control.add(questions_frame, text="Вопросы")
        questions_data = get_all_questions()
        if questions_data:
            self.create_table_view(questions_frame, questions_data, ["question_id", "question_text", "helpful_info"])
        else:
            tk.Label(questions_frame, text="Нет данных о вопросах.", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()

        tab_control.pack(expand=True, fill="both")

    def create_table_view(self, frame, data, columns):
        """Создание и отображение таблицы на основе данных и столбцов."""
        # Создаём таблицу
        table = ttk.Treeview(frame, columns=columns, show="headings")

        # Заголовки таблицы
        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center")  # Выравнивание заголовков по центру

        # Заполнение таблицы данными
        for row in data:
            if isinstance(row, dict):  # Если данные представлены в виде словаря
                values = [row.get(col, "") for col in columns]
            elif hasattr(row, "__dict__"):  # Если данные — это объект SQLAlchemy
                values = [getattr(row, col, "") for col in columns]
            else:
                values = row if isinstance(row, (list, tuple)) else []

            table.insert("", "end", values=values)

        # Устанавливаем таблицу в интерфейс
        table.pack(fill="both", expand=True, pady=10)

    def open_add_dog_window(self):
        """Открыть окно для добавления новой собаки."""
        add_dog_window = tk.Toplevel(self.root)
        add_dog_window.title("Добавить новую собаку")
        add_dog_window.geometry("400x300")
        add_dog_window.configure(bg=BACKGROUND_COLOR)

        tk.Label(add_dog_window, text="Порода", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        breed_entry = tk.Entry(add_dog_window, font=("Comic Sans MS", 12))
        breed_entry.pack(pady=5)

        tk.Label(add_dog_window, text="Характеристики", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        characteristics_entry = tk.Entry(add_dog_window, font=("Comic Sans MS", 12))
        characteristics_entry.pack(pady=5)

        tk.Label(add_dog_window, text="Поведение", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        behavior_entry = tk.Entry(add_dog_window, font=("Comic Sans MS", 12))
        behavior_entry.pack(pady=5)

        tk.Label(add_dog_window, text="Уход", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        care_info_entry = tk.Entry(add_dog_window, font=("Comic Sans MS", 12))
        care_info_entry.pack(pady=5)

        tk.Label(add_dog_window, text="Комментарии администратора", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        admin_comments_entry = tk.Entry(add_dog_window, font=("Comic Sans MS", 12))
        admin_comments_entry.pack(pady=5)

        def save_dog():
            dog_data = {
                'breed': breed_entry.get(),
                'characteristics': characteristics_entry.get(),
                'behavior': behavior_entry.get(),
                'care_info': care_info_entry.get(),
                'admin_comments': admin_comments_entry.get()
            }
            add_dog_to_db(dog_data)
            add_dog_window.destroy()

        def cancel_add():
            add_dog_window.destroy()

        save_button = tk.Button(add_dog_window, text="Сохранить", command=save_dog, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        save_button.pack(pady=20)

        cancel_button = tk.Button(add_dog_window, text="Отменить", command=cancel_add, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        cancel_button.pack(pady=10)


    def open_add_user_window(self):
        """Открыть окно для добавления нового пользователя."""
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Добавить нового пользователя")
        add_user_window.geometry("400x300")
        add_user_window.configure(bg=BACKGROUND_COLOR)

        tk.Label(add_user_window, text="Логин", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        login_entry = tk.Entry(add_user_window, font=("Comic Sans MS", 12))
        login_entry.pack(pady=5)

        tk.Label(add_user_window, text="Пароль", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        password_entry = tk.Entry(add_user_window, font=("Comic Sans MS", 12), show="*")
        password_entry.pack(pady=5)

        tk.Label(add_user_window, text="Имя пользователя", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        username_entry = tk.Entry(add_user_window, font=("Comic Sans MS", 12))
        username_entry.pack(pady=5)

        def save_user():
            user_data = {
                'login': login_entry.get(),
                'password': password_entry.get(),
                'username': username_entry.get(),
            }
            try:
                add_user_to_db(user_data)
                messagebox.showinfo("Успех", "Пользователь успешно добавлен.")
                add_user_window.destroy()
                self.manage_users()  # Обновить список пользователей
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить пользователя: {e}")

        def cancel_add():
            add_user_window.destroy()

        save_button = tk.Button(add_user_window, text="Сохранить", command=save_user, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        save_button.pack(pady=20)

        cancel_button = tk.Button(add_user_window, text="Отменить", command=cancel_add, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        cancel_button.pack(pady=10)

    def open_add_question_window(self):
        """Открыть окно для добавления нового вопроса."""
        add_question_window = tk.Toplevel(self.root)
        add_question_window.title("Добавить новый вопрос")
        add_question_window.geometry("400x300")
        add_question_window.configure(bg=BACKGROUND_COLOR)

        tk.Label(add_question_window, text="ID собаки", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        dog_id_entry = tk.Entry(add_question_window, font=("Comic Sans MS", 12))
        dog_id_entry.pack(pady=5)

        tk.Label(add_question_window, text="Вопрос", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        question_text_entry = tk.Entry(add_question_window, font=("Comic Sans MS", 12))
        question_text_entry.pack(pady=5)

        tk.Label(add_question_window, text="Изображение URL", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        image_url_entry = tk.Entry(add_question_window, font=("Comic Sans MS", 12))
        image_url_entry.pack(pady=5)

        tk.Label(add_question_window, text="Полезная информация", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=10)
        helpful_info_entry = tk.Entry(add_question_window, font=("Comic Sans MS", 12))
        helpful_info_entry.pack(pady=5)

        def save_question():
            question_data = {
                'dog_id': int(dog_id_entry.get()),
                'question_text': question_text_entry.get(),
                'image_url': image_url_entry.get(),
                'helpful_info': helpful_info_entry.get()
            }
            add_question_to_db(question_data)
            add_question_window.destroy()

        def cancel_add():
            add_question_window.destroy()

        save_button = tk.Button(add_question_window, text="Сохранить", command=save_question, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        save_button.pack(pady=20)

        cancel_button = tk.Button(add_question_window, text="Отменить", command=cancel_add, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        cancel_button.pack(pady=10)

