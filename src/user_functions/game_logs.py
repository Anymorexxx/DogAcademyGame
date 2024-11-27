import logging
import os


def setup_logging():
    """Настройка логирования в файл."""
    log_dir = "DogAcademy/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "game.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Логирование игры начато.")
