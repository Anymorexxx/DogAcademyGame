from database.db_events import get_user_progress
from database.db_session import get_session
from sqlalchemy.exc import SQLAlchemyError
from database.models import GameSession


def save_game_session(user_id, level, score, duration, health, hunger, sleepiness):
    """Сохранение игрового процесса в таблицу GameSessions."""
    session = get_session()
    try:
        # Создаем новый объект GameSession
        game_session = GameSession(
            user_id=user_id,
            level=level,
            score=score,
            duration=duration,
            health=health,
            hunger=hunger,
            sleepiness=sleepiness,
        )
        session.add(game_session)
        session.commit()  # Сохраняем данные в таблице
        print(f"Игровой процесс для пользователя {user_id} на уровне {level} успешно сохранен.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка при сохранении игрового процесса: {e}")
    finally:
        session.close()

def print_user_progress(user_id):
    """Печать прогресса пользователя из таблицы GameSessions."""
    progress = get_user_progress(user_id)
    for session in progress:
        print(f"Уровень: {session.level}, Очки: {session.score}, Время: {session.duration} секунд")