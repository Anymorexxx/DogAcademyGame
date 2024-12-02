import logging
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database.db_session import get_session
from database.models import Auth, Notifications, Users, GameSession, Dogs, Questions
from sqlalchemy.exc import SQLAlchemyError


def get_user_by_id(user_id):
    """Получение данных пользователя по ID с предварительной загрузкой связанных данных."""
    session = get_session()
    try:
        user = (
            session.query(Users)
            .options(joinedload(Users.game_sessions))  # Предзагрузка связанных игровых сессий
            .filter_by(user_id=user_id)
            .first()
        )
        return user
    except SQLAlchemyError as e:
        logging.error(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        session.close()

def create_user(login, password, username):
    """Регистрация нового пользователя."""
    session = get_session()

    # Проверка, есть ли уже пользователь с таким логином
    if session.query(Auth).filter_by(login=login).first():
        return False, "Логин уже используется."

    # Создаём новую запись в таблице Auth
    new_auth = Auth(login=login, password=password)
    session.add(new_auth)

    try:
        session.commit()  # Сохраняем изменения в таблице Auth

        # Создаём новую запись в таблице Users, связываем с только что добавленным Auth
        new_user = Users(user_id=new_auth.user_id, username=username)
        session.add(new_user)
        session.commit()  # Сохраняем изменения в таблице Users

        # Создаём новый игровой процесс для этого пользователя
        new_game_session = GameSession(user_id=new_user.user_id, level=1)  # Устанавливаем уровень по умолчанию
        session.add(new_game_session)
        session.commit()  # Сохраняем данные в GameSession

        print(f"Пользователь {username} успешно добавлен!")
        return True, "Регистрация успешна."

    except SQLAlchemyError as e:
        session.rollback()  # Откат изменений при ошибке
        print(f"Ошибка при создании пользователя: {e}")
        return False, "Произошла ошибка при регистрации."
    finally:
        session.close()



def check_user(login, password=None):
    session = get_session()
    try:
        query = session.query(Auth).filter_by(login=login)
        if password:
            query = query.filter_by(password=password)
        user = query.first()
        if user:
            return user.user_id
        else:
            return None
    except SQLAlchemyError as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None
    finally:
        session.close()

def save_progress(user_id, level, score, duration, health, hunger, sleepiness):
    """Сохранение игрового прогресса в базу данных."""
    session = get_session()
    try:
        if not user_id:
            raise ValueError("user_id не указан!")
        session_data = GameSession(
            user_id=user_id,
            level=level,
            score=score,
            duration=duration,
            health=health,
            hunger=hunger,
            sleepiness=sleepiness,
            end_time=func.now()
        )
        session.add(session_data)
        session.commit()
    except SQLAlchemyError as e:
        logging.error(f"Ошибка при сохранении прогресса: {e}")
        session.rollback()
    except ValueError as e:
        logging.error(e)
    finally:
        session.close()

def get_user_progress(user_id):
    """Получение игрового прогресса пользователя."""
    session = get_session()
    try:
        return session.query(GameSession).filter_by(user_id=user_id).all()
    except Exception as e:
        logging.error(f"Ошибка при получении прогресса пользователя: {e}")
        return []
    finally:
        session.close()

def create_notification(user_id, message):
    """Создание уведомления для пользователя."""
    session = get_session()
    try:
        notification = Notifications(user_id=user_id, message=message)
        session.add(notification)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Ошибка при создании уведомления: {e}")
        session.rollback()
    finally:
        session.close()

def get_notifications(user_id):
    """Получение уведомлений для пользователя."""
    session = get_session()
    try:
        notifications = session.query(Notifications).filter_by(user_id=user_id).all()
        return notifications
    except SQLAlchemyError as e:
        print(f"Ошибка при получении уведомлений: {e}")
        return []
    finally:
        session.close()

def get_knowledge_base():
    """Получение базы знаний (статей о собаках)."""
    session = get_session()
    try:
        dogs = session.query(Dogs).all()
        return dogs  # Список объектов Dogs
    except SQLAlchemyError as e:
        print(f"Ошибка при получении базы знаний: {e}")
        return []
    finally:
        session.close()

def get_dogs():
    """Получение списка пород собак."""
    session = get_session()
    try:
        dogs = session.query(Dogs).all()
        return dogs  # Список объектов Dogs
    except SQLAlchemyError as e:
        print(f"Ошибка при получении списка собак: {e}")
        return []
    finally:
        session.close()

def update_user_dog(user_id, dog_id):
    """Обновление выбранной пользователем породы собаки."""
    session = get_session()
    try:
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            user.dog_id = dog_id
            session.commit()
            print(f"Порода пользователя обновлена на {dog_id}")
        else:
            print("Пользователь не найден.")
    except SQLAlchemyError as e:
        print(f"Ошибка при обновлении породы собаки: {e}")
        session.rollback()
    finally:
        session.close()

def debug_list_users():
    """Отладочный вывод всех пользователей."""
    session = get_session()
    try:
        users = session.query(Auth).all()
        for user in users:
            print(f"User ID: {user.user_id}, Login: {user.login}, Password: {user.password}")
    except SQLAlchemyError as e:
        print(f"Ошибка при получении списка пользователей: {e}")
    finally:
        session.close()

def get_all_users():
    """Получить всех пользователей с предварительной загрузкой данных."""
    session = get_session()
    try:
        users = session.query(Users).options(joinedload(Users.auth)).all()
        return users
    except SQLAlchemyError as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []  # Возвращаем пустой список, если ошибка
    finally:
        session.close()

def get_all_questions():
    """Получить все вопросы."""
    session = get_session()
    try:
        questions = session.query(Questions).all()
        return questions
    except SQLAlchemyError as e:
        print(f"Ошибка при получении вопросов: {e}")
        return []
    finally:
        session.close()

def get_all_dogs():
    """Получить все записи о собаках."""
    session = get_session()
    try:
        dogs = session.query(Dogs).all()
        return dogs
    except SQLAlchemyError as e:
        print(f"Ошибка при получении собак: {e}")
        return []
    finally:
        session.close()

def get_user_by_username(username):
    """Получить пользователя по логину."""
    session = get_session()
    try:
        user = session.query(Users).join(Auth).filter(Auth.login == username).first()
        return user
    except SQLAlchemyError as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        session.close()

def update_user(user_id, new_login, new_password):
    """Обновить данные пользователя."""
    session = get_session()
    try:
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            auth = user.auth
            auth.login = new_login
            auth.password = new_password
            session.commit()
    except SQLAlchemyError as e:
        print(f"Ошибка при обновлении пользователя: {e}")
        session.rollback()
    finally:
        session.close()

def update_user_info(user_id, new_login, new_username):
    """Обновление данных пользователя."""
    session = get_session()
    try:
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            user.auth.login = new_login
            user.username = new_username
            session.commit()
            return True, "Данные пользователя обновлены."
        return False, "Пользователь не найден."
    except SQLAlchemyError as e:
        session.rollback()
        return False, f"Ошибка при обновлении: {e}"
    finally:
        session.close()


def delete_user(user_id):
    """Удаление пользователя."""
    session = get_session()
    try:
        user = session.query(Users).filter_by(user_id=user_id).first()
        if user:
            session.delete(user.auth)
            session.commit()
            return True, "Пользователь удалён."
        return False, "Пользователь не найден."
    except SQLAlchemyError as e:
        session.rollback()
        return False, f"Ошибка при удалении: {e}"
    finally:
        session.close()


def update_dog_info(dog_id, breed, characteristics):
    """Обновление информации о собаке."""
    session = get_session()
    try:
        dog = session.query(Dogs).filter_by(dog_id=dog_id).first()
        if dog:
            dog.breed = breed
            dog.characteristics = characteristics
            session.commit()
            return True, "Информация о собаке обновлена."
        return False, "Собака не найдена."
    except SQLAlchemyError as e:
        session.rollback()
        return False, f"Ошибка при обновлении: {e}"
    finally:
        session.close()


def update_question(question_id, text, helpful_info):
    """Обновление вопроса."""
    session = get_session()
    try:
        question = session.query(Questions).filter_by(question_id=question_id).first()
        if question:
            question.question_text = text
            question.helpful_info = helpful_info
            session.commit()
            return True, "Вопрос обновлён."
        return False, "Вопрос не найден."
    except SQLAlchemyError as e:
        session.rollback()
        return False, f"Ошибка при обновлении: {e}"
    finally:
        session.close()