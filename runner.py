from quiz.engine import Engine
from quiz.logging_config import setup_logging

# Налаштування логування
setup_logging()

# Створення і запуск двигуна вікторини
engine = Engine()
engine.run()
