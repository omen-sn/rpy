import os
from pathlib import Path
import logging


class FileWriter:
    def __init__(self, mode, filename='file.txt', answers_dir=None):
        self.mode = mode
        self.filename = filename
        if answers_dir is None:
            self.answers_dir = Path(__file__).resolve().parent.parent / 'answers'
        else:
            self.answers_dir = Path(answers_dir)

    def write(self, message):
        try:
            # Створюємо директорію, якщо вона не існує
            self.answers_dir.mkdir(parents=True, exist_ok=True)
            # Відкриваємо файл для запису
            with open(self.answers_dir / self.filename, self.mode, encoding='utf-8') as file:
                file.write(message + '\n')  # Додаємо '\n' для запису повідомлення в новому рядку
            logging.info(f"Повідомлення успішно записано в {self.filename}")
        except Exception as e:
            logging.error(f"Помилка при записі в файл {self.filename}: {e}")

# Приклад використання
# writer = FileWriter('w', 'test.txt')
# writer.write('Hello, Quiz!')