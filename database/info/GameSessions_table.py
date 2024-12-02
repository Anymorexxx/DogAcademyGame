import logging
from sqlalchemy import func
from database.db_events import get_user_progress
from database.db_session import get_session
from sqlalchemy.exc import SQLAlchemyError
from database.models import GameSession


def save_game_session(user_id, level, score, steps, duration=0, health=100, hunger=0, sleepiness=0):
    """Сохранение игрового прогресса."""
    session = get_session()
    try:
        session.add(GameSession(
            user_id=user_id,
            level=level,
            score=score,
            steps=steps,
            duration=duration,
            health=health,
            hunger=hunger,
            sleepiness=sleepiness
        ))
        session.commit()
        logging.info(f"Сессия сохранена: user_id={user_id}, level={level}, score={score}")
    except Exception as e:
        session.rollback()
        logging.error(f"Ошибка при сохранении игровой сессии: {e}")
        raise


def print_user_progress(user_id):
    """
    Печать прогресса пользователя из таблицы GameSessions.

    :param user_id: ID пользователя
    """
    if not user_id:
        logging.error("user_id отсутствует. Невозможно получить прогресс.")
        return

    progress = get_user_progress(user_id)
    if not progress:
        print(f"У пользователя с ID {user_id} нет сохраненного прогресса.")
        return

    print(f"Прогресс пользователя (user_id={user_id}):")
    for session in progress:
        print(f"- Уровень: {session.level}, Очки: {session.score}, Время: {session.duration} сек")
