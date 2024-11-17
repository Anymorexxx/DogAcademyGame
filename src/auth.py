from database.db_session import session
from database.models import Auth, Users

def register_user(login, password, username):
    if session.query(Auth).filter_by(login=login).first():
        return False, "Логин уже используется."
    new_auth = Auth(login=login, password=password)
    session.add(new_auth)
    session.commit()
    new_user = Users(user_id=new_auth.user_id, username=username)
    session.add(new_user)
    session.commit()
    return True, "Регистрация успешна."

def login_user(login, password):
    user = session.query(Auth).filter_by(login=login, password=password).first()
    if user:
        return True, user.user_id
    return False, "Неверный логин или пароль."
