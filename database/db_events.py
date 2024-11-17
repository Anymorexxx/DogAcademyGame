from database.db_session import get_session
from database.models import Auth
from sqlalchemy.exc import SQLAlchemyError

def create_user(login, password):
    """Создание нового пользователя в базе данных."""
    session = get_session()
    try:
        new_user = Auth(login=login, password=password)
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
        return user is not None
    except SQLAlchemyError as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        session.close()
