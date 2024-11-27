# Админ-интерфейс (тёмные цвета)
ADMIN_BACKGROUND_COLOR = "#403d49"
ADMIN_PRIMARY_COLOR = "#ff6347"
ADMIN_BUTTON_COLOR = "#444444"
ADMIN_BUTTON_TEXT_COLOR = "#ffffff"
ADMIN_FONT = ("Comic Sans MS", 25)
ADMIN_BIG_FONT = ("Comic Sans MS", 40)

# Интерфейс пользователя (АВТОРИЗАЦИЯ)
BACKGROUND_COLOR = "#f8e1e1"
PRIMARY_COLOR = "#ff6347"
BUTTON_COLOR = "#87ceeb"
BUTTON_TEXT_COLOR = "white"
FONT = ("Comic Sans MS", 25)
BIG_FONT = ("Comic Sans MS", 40)

# ГЛАВНОЕ МЕНЮ
BACKGROUND_COLOR_USER = "#bcabe5"  # Основной фон
TOP_PANEL_COLOR_USER = "#aa9bcd"  # Цвет верхней панели
BUTTON_COLOR_PROFILE_USER = "#a2c792"  # Цвет кнопок "Профиль", "Магазин", "База знаний"
BUTTON_COLOR_PLAY_USER = "#b4e1a1"  # Цвет кнопки "Играть"
BUTTON_COLOR_EXIT_USER = "#a2c792"  # Цвет кнопки "Выход"
BUTTON_TEXT_COLOR_USER = "white"  # Цвет текста на кнопках
FONT_USER = ("Comic Sans MS", 20)  # Шрифт для текста кнопок
BIG_FONT_USER = ("Comic Sans MS", 30)  # Большой шрифт (например, для заголовков)
BUTTON_RADIUS_USER = 50  # Радиус круглой кнопки
EXIT_BUTTON_SIZE_USER = (80, 40)  # Размер кнопки "Выход"
TOP_PANEL_COLOR = "#BBA0D0"
BUTTON_COLOR_PROFILE = "#8FC085"
BUTTON_COLOR_PLAY = "#8FC085"
BUTTON_COLOR_EXIT = "#8FC085"
# Размеры
PLAY_BUTTON_RADIUS = 100
EXIT_BUTTON_WIDTH = 100
EXIT_BUTTON_HEIGHT = 50

# Данные для авторизации администратора
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin123"

# База данных
DATABASE_URL = "sqlite:///F:/Projects/Dog_Academy/database/DogAcademy.db"  # Абсолютный путь

# Иконки
SETTINGS_IMG = "assets/settings.png"
LOGO = "F:/Projects/Dog_Academy/assets/logo.png"
BACKGROUND_GAME = "F:/Projects/Dog_Academy/assets/background.png"
BONE = "F:/Projects/Dog_Academy/assets/bone.png"
LOCK = "F:/Projects/Dog_Academy/assets/lock.png"
UNLOCK = "F:/Projects/Dog_Academy/assets/unlock.png"
DONE = "F:/Projects/Dog_Academy/assets/done.png"

# Собаки
CHIHUAHUA = "F:/Projects/Dog_Academy/assets/dogs/Chihuahua.png"
CORGI = "F:/Projects/Dog_Academy/assets/dogs/Corgi.png"
RETRIEVER = "F:/Projects/Dog_Academy/assets/dogs/Golden_Retriever.png"
HUSKY = "F:/Projects/Dog_Academy/assets/dogs/Husky.png"
POMERANIAN = "F:/Projects/Dog_Academy/assets/dogs/Pomeranian.png"
PUG = "F:/Projects/Dog_Academy/assets/dogs/Pug.png"
YORKSHIRE = "F:/Projects/Dog_Academy/assets/dogs/Yorkshire_Terrier.png"

DOG_CHARACTERS = {
    "Chihuahua": {
        "image": CHIHUAHUA,
        "speed": 8,
        "endurance": 5,
        "special_ability": "Fast Dodge",  # Уклонение от препятствий
    },
    "Corgi": {
        "image": CORGI,
        "speed": 6,
        "endurance": 7,
        "special_ability": "Extra Jump",  # Дополнительный прыжок
    },
    "Golden Retriever": {
        "image": RETRIEVER,
        "speed": 7,
        "endurance": 8,
        "special_ability": "Bonus Points",  # Увеличенные очки за правильные ответы
    },
    "Husky": {
        "image": HUSKY,
        "speed": 9,
        "endurance": 6,
        "special_ability": "Speed Boost",  # Ускорение
    },
    "Pomeranian": {
        "image": POMERANIAN,
        "speed": 7,
        "endurance": 4,
        "special_ability": "Charm",  # Уменьшает штраф за ошибки
    },
    "Pug": {
        "image": PUG,
        "speed": 5,
        "endurance": 9,
        "special_ability": "Resilience",  # Сохраняет здоровье при столкновениях
    },
    "Yorkshire Terrier": {
        "image": YORKSHIRE,
        "speed": 6,
        "endurance": 5,
        "special_ability": "Quick Recovery",  # Быстрое восстановление характеристик
    },
}

# Утилиты
NOTIFICATION_LEVEL = "info"  # Возможные значения: "info", "warning", "error"
USE_DATABASE_LOGS = True

# Игровые параметры
INITIAL_SCORE = 5  # Начальные очки игрока
POINTS_CORRECT_ANSWER = 2  # Очки за правильный ответ
POINTS_WRONG_ANSWER = -1  # Штраф за неправильный ответ
MAX_LEVELS = 100  # Максимальное количество уровней
INITIAL_DOG_STATUS = {"health": 100, "hunger": 0, "sleepiness": 0}  # Стартовые характеристики собаки

# Параметры карты
MIN_OBSTACLES = 3  # Минимум препятствий на уровне
MAX_OBSTACLES = 6  # Максимум препятствий на уровне

# Графика и анимация
COUNTDOWN_DURATION = 3  # Продолжительность обратного отсчёта в секундах
