import logging
from database.db_events import get_user_progress
from database.db_session import get_session
from database.models import GameSession


def save_game_session(user_id, level, score, duration, steps, health, hunger, sleepiness):
    """Сохранение игрового прогресса с обновлением существующей записи."""
    session = get_session()  # Получаем сессию для работы с базой данных
    try:
        # Проверяем, существует ли уже запись для данного пользователя и уровня
        existing_session = session.query(GameSession).filter_by(user_id=user_id, level=level).first()
        if existing_session:
            logging.info(f"Обновление прогресса для user_id={user_id}, level={level}.")
            existing_session.score = score
            existing_session.duration = duration
            existing_session.steps = steps
            existing_session.health = health
            existing_session.hunger = hunger
            existing_session.sleepiness = sleepiness
        else:
            # Если записи нет, создаем новую
            new_session = GameSession(
                user_id=user_id,
                level=level,
                score=score,
                duration=duration,
                steps=steps,
                health=health,
                hunger=hunger,
                sleepiness=sleepiness
            )
            session.add(new_session)  # Добавляем в сессию
        session.commit()  # Сохраняем изменения в базе данных
        logging.info(f"Прогресс успешно сохранён: user_id={user_id}, level={level}, score={score}")
    except Exception as e:
        session.rollback()  # Откатываем изменения в случае ошибки
        logging.error(f"Ошибка при сохранении прогресса: {e}")
    finally:
        session.close()  # Закрываем сессию



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
