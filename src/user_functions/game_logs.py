import logging
import os


def setup_logging():
    """Настройка логирования в файл."""
    log_file = "logs/game.log"
    if not os.path.exists(log_file):
        os.makedirs(log_file)

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Логирование игры начато.")
