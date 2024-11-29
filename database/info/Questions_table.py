from database.db_session import get_session
from database.models import Dogs, Questions

DOG_QUESTIONS = {
    "Chihuahua": [
        {
            "question_text": "Почему у Чихуахуа часто возникают проблемы с зубами?",
            "helpful_info": "Миниатюрный размер приводит к скоплению налета и зубных отложений.",
        },
        {
            "question_text": "Какая активность лучше всего подходит для Чихуахуа?",
            "helpful_info": "Легкие прогулки и домашние игры.",
        }
    ],
    "Corgi": [
        {
            "question_text": "Почему важно контролировать вес Корги?",
            "helpful_info": "Избыточный вес может негативно повлиять на суставы.",
        },
        {
            "question_text": "Как можно поддерживать здоровье суставов у Корги?",
            "helpful_info": "Обеспечьте умеренную активность и сбалансированное питание.",
        }
    ],
    "Golden Retriever": [
        {
            "question_text": "Почему важно регулярно вычесывать шерсть Голден Ретривера?",
            "helpful_info": "Это предотвращает образование колтунов.",
        },
        {
            "question_text": "Какое питание подходит для Голден Ретриверов?",
            "helpful_info": "Сбалансированное питание с учетом активности и возраста.",
        }
    ],
    "Husky": [
        {
            "question_text": "Какой климат подходит для Хаски?",
            "helpful_info": "Они комфортнее чувствуют себя в холодном климате.",
        },
        {
            "question_text": "Почему Хаски требуют много физической активности?",
            "helpful_info": "Эта порода обладает высокой энергией и выносливостью.",
        }
    ],
    "Pomeranian": [
        {
            "question_text": "Как правильно ухаживать за шерстью Померанского шпица?",
            "helpful_info": "Ежедневно расчесывать шерсть, чтобы избежать колтунов.",
        },
        {
            "question_text": "Почему важно следить за зубами Померанского шпица?",
            "helpful_info": "Они склонны к зубному налету, что может привести к проблемам.",
        }
    ],
    "Pug": [
        {
            "question_text": "Почему мопсы склонны к ожирению?",
            "helpful_info": "Их низкая активность и любовь к еде требуют контроля рациона.",
        },
        {
            "question_text": "Какие проблемы с дыханием могут возникнуть у мопсов?",
            "helpful_info": "Из-за их плоской морды дыхание может быть затруднено.",
        }
    ],
    "Yorkshire Terrier": [
        {
            "question_text": "Как часто нужно стричь шерсть Йоркширского терьера?",
            "helpful_info": "Примерно раз в 4-6 недель для поддержания аккуратного вида.",
        },
        {
            "question_text": "Как ухаживать за шерстью Йоркширского терьера?",
            "helpful_info": "Регулярно расчесывать и использовать специальные средства.",
        }
    ]
}

def populate_questions():
    session = get_session()
    try:
        dogs = {dog.breed: dog.dog_id for dog in session.query(Dogs).all()}
        for breed, questions in DOG_QUESTIONS.items():
            dog_id = dogs.get(breed)
            if not dog_id:
                print(f"Порода '{breed}' отсутствует.")
                continue
            for question_data in questions:
                question = Questions(
                    dog_id=dog_id,
                    question_text=question_data["question_text"],
                    helpful_info=question_data["helpful_info"]
                )
                session.add(question)
        session.commit()
        print("Таблица Questions успешно заполнена.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при заполнении Questions: {e}")
    finally:
        session.close()
