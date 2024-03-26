import os
from pathlib import Path
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileWriter:
    def __init__(self, mode, filename, answers_dir='answers'):
        self.mode = mode
        self.filename = filename
        # Змінено для використання Pathlib
        self.answers_dir = Path(__file__).resolve().parent.parent / answers_dir

    def write(self, message):
        try:
            # Створюємо директорію, якщо вона не існує
            self.answers_dir.mkdir(parents=True, exist_ok=True)
            # Відкриваємо файл для запису
            with open(self.answers_dir / self.filename, self.mode) as file:
                file.write(message + '\n')  # Додаємо '\n' для запису повідомлення в новому рядку
            logging.info(f"Повідомлення успішно записано в {self.filename}")
        except Exception as e:
            logging.error(f"Помилка при записі в файл {self.filename}: {e}")

# Приклад використання
# writer = FileWriter('w', 'test.txt')
# writer.write('Hello, Quiz!')
