from database.db_session import get_session, init_db
from database.info.Dogs_table import populate_dogs
from database.info.Questions_table import populate_questions
from database.models import Dogs, Questions


def test_data_integrity():
    session = get_session()
    try:
        # Проверяем, есть ли собаки
        dogs = session.query(Dogs).all()
        assert len(dogs) > 0, "Таблица Dogs пуста!"

        # Проверяем, есть ли вопросы
        questions = session.query(Questions).all()
        assert len(questions) > 0, "Таблица Questions пуста!"

        # Проверяем связь вопросов с породами
        for question in questions:
            assert question.dog_id is not None, f"У вопроса {question.question_id} отсутствует dog_id"
            dog = session.query(Dogs).filter_by(dog_id=question.dog_id).first()
            assert dog is not None, f"Ссылка на несуществующую собаку в вопросе {question.question_id}"

        print("Все тесты успешно пройдены.")
    except AssertionError as e:
        print(f"Ошибка теста: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Инициализируем базу данных (пересоздаём таблицы для чистого теста)
    init_db(refresh=True)

    # Заполняем таблицы
    populate_dogs()
    populate_questions()

    # Запускаем тесты
    test_data_integrity()
