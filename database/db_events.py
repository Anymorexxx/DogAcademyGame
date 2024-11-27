from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database.db_session import get_session
from database.models import Auth, Notifications, Users, GameSession, Dogs, Questions
from sqlalchemy.exc import SQLAlchemyError

def create_user(login, password, username):
    """Создание нового пользователя в базе данных."""
    session = get_session()
    try:
        new_user_auth = Auth(login=login, password=password)
        session.add(new_user_auth)
        session.commit()

        new_user = Users(username=username, auth=new_user_auth)
        session.add(new_user)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Ошибка при создании пользователя: {e}")
        session.rollback()
    finally:
        session.close()

def check_user(login, password):
    """Проверка данных пользователя для авторизации."""
    session = get_session()
    try:
        user = session.query(Auth).filter_by(login=login, password=password).first()
        if user:
            return user.user_id  # Получаем user_id из Auth
        return None
    except SQLAlchemyError as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None
    finally:
        session.close()

def save_progress(user_id, level, score, duration, health, hunger, sleepiness):
    """Сохраняет прогресс пользователя в базу данных."""
    session = get_session()
    try:
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
        print(f"Ошибка при сохранении прогресса: {e}")
        session.rollback()
    finally:
        session.close()

def get_user_progress(user_id):
    """Получение прогресса пользователя по его ID."""
    session = get_session()
    try:
        progress = session.query(GameSession).filter_by(user_id=user_id).all()
        return progress
    except SQLAlchemyError as e:
        print(f"Ошибка при получении прогресса: {e}")
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
