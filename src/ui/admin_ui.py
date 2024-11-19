import tkinter as tk
from PIL import Image, ImageTk
from config import SETTINGS_IMG
from src.admin_functions import db_management, admin_logging, statistics, content, knowledge_base
from src.utils import clear_frame  # Импортируем общую функцию для очистки фрейма


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
        self.create_nav_button("Логирование", admin_logging.show_logs)
        self.create_nav_button("Статистика", statistics.show_statistics)
        self.create_nav_button("Уведомления", self.show_notifications)
        self.create_nav_button("Безопасность", self.show_security)

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
            command=self.toggle_menu  # Проверьте, что эта команда правильно привязана
        )
        self.menu_button.pack(side="right", padx=10, pady=10)

        # Основное окно
        self.main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        # Бургер-меню (скрытое по умолчанию)
        self.menu_frame = tk.Frame(self.root, bg=MENU_COLOR, width=300)
        self.menu_frame.place(x=1620, y=60, width=300, height=1020)  # Явно задаём ширину и высоту
        self.menu_frame.lower()  # Прячем меню
        self.menu_visible = False  # Добавлен флаг для отслеживания состояния меню

    def toggle_menu(self):
        """Показ или скрытие меню."""
        print(
            f"Кнопка меню нажата. Меню сейчас {'видимо' if self.menu_visible else 'скрыто'}")  # Отладка
        if self.menu_visible:  # Используем флаг для проверки состояния
            print("Скрываем меню")  # Отладка
            self.menu_frame.lower()  # Скрываем меню
            self.menu_visible = False
        else:
            print("Показываем меню")  # Отладка
            self.menu_frame.lift()  # Показываем меню
            self.menu_visible = True
            self.populate_menu()  # Наполнение меню элементами

    def populate_menu(self):
        # Очистка меню
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        # Создание пунктов меню
        self.create_menu_section("Работа с базой данных", [
            ("Редактирование пользователей", db_management.edit_users),
            ("Управление вопросами", db_management.manage_questions),
            ("Просмотр таблиц", db_management.view_tables),
        ])
        self.create_menu_section("Управление игровым контентом", [
            ("Создание и настройка уровней", content.manage_levels),
            ("Настройка параметров собаки", content.manage_dog_params),
        ])
        self.create_menu_section("Управление интерфейсом пользователя", [
            ("Изменение цветовой схемы, фона и логотипа", self.change_ui_settings),
            ("Добавление подсказок в интерфейс", self.manage_ui_tips),
        ])
        self.create_menu_section("Работа с базой знаний", [
            ("Добавление информации", knowledge_base.add_info),
            ("Редактирование записей", knowledge_base.edit_records),
            ("Удаление записей", knowledge_base.delete_records),
            ("Просмотр базы знаний", knowledge_base.view_knowledge_base),
            ("Генерация вопросов", knowledge_base.generate_questions),
        ])

    def create_menu_section(self, title, items):
        section_label = tk.Label(self.menu_frame, text=title, bg=MENU_COLOR, fg=TEXT_COLOR, font=("Comic Sans MS", 14, "bold"))
        section_label.pack(anchor="w", padx=10, pady=5)

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
                command=lambda: command(self.main_frame)  # Вызываем функцию и передаём фрейм
            )
            item_button.pack(anchor="w", padx=20, pady=2)

    def create_nav_button(self, text, command):
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
            command=lambda: command(self.main_frame)  # Вызываем переданную функцию
        )
        button.pack(side="left", padx=10, pady=10)

    def manage_ui_tips(self, frame):
        # Пример логики для управления подсказками
        print("Управление подсказками интерфейса.")
        # Код для управления подсказками (например, скрытие или показ подсказок)
        tk.Label(frame, text="Здесь будут подсказки для интерфейса", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Comic Sans MS", 16)).pack()

    def show_notifications(self, frame):
        clear_frame(frame)
        tk.Label(frame, text="Здесь будут уведомления", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Comic Sans MS", 16)).pack()

    def show_security(self, frame):
        clear_frame(frame)
        tk.Label(frame, text="Раздел Безопасность", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=("Comic Sans MS", 16)).pack()

    def change_ui_settings(self, frame):
        clear_frame(frame)
        """Метод для изменения цветовой схемы, фона и логотипа"""
        print("Изменение UI настроек")  # Пока просто тестовый вывод
