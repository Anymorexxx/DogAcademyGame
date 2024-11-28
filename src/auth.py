from sqlalchemy.exc import SQLAlchemyError
from database.db_session import get_session
from database.models import Auth, Users, GameSession


def register_user(login, password, username):
    """Регистрация нового пользователя."""
    session = get_session()

    # Проверяем, есть ли уже пользователь с таким логином
    if session.query(Auth).filter_by(login=login).first():
        return False, "Логин уже используется."

    # Создаем новую запись в таблице Auth
    new_auth = Auth(login=login, password=password)
    session.add(new_auth)

    try:
        session.commit()  # Сохраняем изменения в таблице Auth

        # Создаем новую запись в таблице Users, связывая с только что добавленным Auth
        # Используем new_auth.user_id для связи
        new_user = Users(user_id=new_auth.user_id, username=username)
        session.add(new_user)
        session.commit()  # Сохраняем изменения в таблице Users

        # Создаем новый игровой процесс в GameSession для этого пользователя
        new_game_session = GameSession(user_id=new_user.user_id, level=1)  # Устанавливаем уровень по умолчанию
        session.add(new_game_session)
        session.commit()  # Сохраняем данные в GameSession

        print(f"Пользователь {username} успешно добавлен!")
    except SQLAlchemyError as e:
        session.rollback()  # Откат изменений при ошибке
        print(f"Ошибка при создании пользователя: {e}")
        return False, "Произошла ошибка при регистрации."
    finally:
        session.close()

    return True, "Регистрация успешна."


def login_user(login, password):
    """Авторизация пользователя."""
    session = get_session()

    # Проверяем, существует ли пользователь с таким логином и паролем
    user_auth = session.query(Auth).filter_by(login=login, password=password).first()

    if user_auth:
        # Возвращаем успешный вход и ID пользователя из таблицы Users
        user = session.query(Users).filter_by(user_id=user_auth.user_id).first()
        return True, user.user_id

    return False, "Неверный логин или пароль."
