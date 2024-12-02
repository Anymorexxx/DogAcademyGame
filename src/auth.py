import logging

from sqlalchemy.exc import SQLAlchemyError
from database.db_session import get_session
from database.models import Auth, Users, GameSession


def register_user(login, password, username):
    """Регистрация нового пользователя."""
    session = get_session()
    try:
        if session.query(Auth).filter_by(login=login).first():
            return False, "Логин уже используется."

        # Создаем новую запись в Auth
        new_auth = Auth(login=login, password=password)
        session.add(new_auth)
        session.commit()

        # Создаем запись в Users
        new_user = Users(user_id=new_auth.user_id, username=username)
        session.add(new_user)

        # Создаем запись в GameSession
        new_game_session = GameSession(user_id=new_user.user_id, level=1)
        session.add(new_game_session)
        session.commit()

        return True, "Регистрация успешна."
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Ошибка при регистрации: {e}")
        return False, "Произошла ошибка при регистрации."
    finally:
        session.close()


def login_user(login, password):
    """Авторизация пользователя."""
    session = get_session()
    try:
        auth = session.query(Auth).filter_by(login=login, password=password).first()
        if auth:
            return True, auth.user_id
        return False, "Неверный логин или пароль."
    except SQLAlchemyError as e:
        return False, f"Ошибка авторизации: {e}"
    finally:
        session.close()
