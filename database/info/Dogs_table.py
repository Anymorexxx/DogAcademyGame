import logging

from sqlalchemy.exc import SQLAlchemyError

from database.db_session import get_session
from database.models import Dogs

DOG_CHARACTERS = {
    "Chihuahua": {
        "characteristics": "Скорость: 8, Выносливость: 5, Умение: Быстрое уклонение.",
        "behavior": "Энергичный, часто лайливый.",
        "care_info": "Нуждается в регулярной чистке зубов и когтей.",
        "admin_comments": "Идеален для активных владельцев."
    },
    "Corgi": {
        "characteristics": "Скорость: 6, Выносливость: 7, Умение: Дополнительный прыжок.",
        "behavior": "Дружелюбный, легко обучаемый.",
        "care_info": "Важно контролировать вес из-за коротких лап.",
        "admin_comments": "Подходит для семей с детьми."
    },
    "Golden Retriever": {
        "characteristics": "Скорость: 7, Выносливость: 8, Умение: Увеличенные очки за правильные ответы.",
        "behavior": "Очень умный и добрый.",
        "care_info": "Требует регулярной чистки шерсти.",
        "admin_comments": "Идеален для владельцев, ищущих верного друга."
    },
    "Husky": {
        "characteristics": "Скорость: 9, Выносливость: 6, Умение: Ускорение.",
        "behavior": "Независимый, требует много активности.",
        "care_info": "Плохо переносит жару, требует частых прогулок.",
        "admin_comments": "Для опытных владельцев."
    },
    "Pomeranian": {
        "characteristics": "Скорость: 7, Выносливость: 4, Умение: Уменьшение штрафа за ошибки.",
        "behavior": "Веселый, преданный.",
        "care_info": "Шерсть требует ежедневного ухода.",
        "admin_comments": "Идеален для жизни в квартире."
    },
    "Pug": {
        "characteristics": "Скорость: 5, Выносливость: 9, Умение: Сохраняет здоровье при столкновениях.",
        "behavior": "Ласковый, склонен к перееданию.",
        "care_info": "Внимание к дыханию и физической активности.",
        "admin_comments": "Для спокойного образа жизни."
    },
    "Yorkshire Terrier": {
        "characteristics": "Скорость: 6, Выносливость: 5, Умение: Быстрое восстановление характеристик.",
        "behavior": "Компактный, умный.",
        "care_info": "Требует профессиональной стрижки.",
        "admin_comments": "Подходит для маленьких пространств."
    }
}

def populate_dogs():
    """
    Заполнение таблицы Dogs предустановленными данными.
    """
    session = get_session()
    try:
        logging.info("Начинается заполнение таблицы Dogs.")
        for breed, data in DOG_CHARACTERS.items():
            existing_dog = session.query(Dogs).filter_by(breed=breed).first()
            if not existing_dog:
                dog = Dogs(
                    breed=breed,
                    characteristics=data['characteristics'],
                    behavior=data['behavior'],
                    care_info=data['care_info'],
                    admin_comments=data['admin_comments']
                )
                session.add(dog)
        session.commit()
        logging.info("Таблица Dogs успешно заполнена.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Ошибка при заполнении Dogs: {e}")
    finally:
        session.close()


def get_all_dogs():
    """
    Получение списка всех пород собак из базы данных.

    :return: Список объектов Dogs.
    """
    session = get_session()
    try:
        dogs = session.query(Dogs).all()
        return dogs
    except SQLAlchemyError as e:
        logging.error(f"Ошибка при получении списка собак: {e}")
        return []
    finally:
        session.close()
