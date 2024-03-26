import json
import yaml
import logging
import threading
import glob
import os
from pathlib import Path
from quiz.models.question import Question


class QuestionData:
    def __init__(self, yaml_dir=Path(__file__).resolve().parent.parent / 'yml', in_ext='yml'):
        # Встановлення шляху до папки з YAML файлами
        self.yaml_dir = yaml_dir
        self.in_ext = in_ext
        self.collection = []
        self.threads = []
        self.load_data()

    def save_to_yaml(self, filename='questions_output.yaml'):
        try:
            with open(self.prepare_filename(filename), 'w', encoding='utf-8') as f:
                yaml.dump([q.to_dict() for q in self.collection], f, default_flow_style=False)
            logging.info(f"Дані успішно збережено у файл {filename}")
        except Exception as e:
            logging.error(f"Помилка при збереженні у YAML: {e}")

    def save_to_json(self, filename='questions_output.json'):
        try:
            with open(self.prepare_filename(filename), 'w', encoding='utf-8') as f:
                json.dump([q.to_dict() for q in self.collection], f, indent=2)
            logging.info(f"Дані успішно збережено у файл {filename}")
        except Exception as e:
            logging.error(f"Помилка при збереженні у JSON: {e}")

    def each_file(self):
        pattern = f"*.{self.in_ext}"
        return glob.glob(os.path.join(self.yaml_dir, pattern))

    def load_data(self):
        files = self.each_file()
        if not files:
            logging.warning("Файли для завантаження не знайдено.")
            return

        for filename in files:
            self.in_thread(self.load_from, filename)

        for thread in self.threads:
            thread.join()

    def load_from(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                questions = yaml.safe_load(f)
            for question in questions:
                self.collection.append(Question(question['question'], question['answers']))
            logging.info(f"Дані з файлу {filename} завантажено.")
        except Exception as e:
            logging.error(f"Не вдалося завантажити дані з {filename}: {e}")

    def in_thread(self, func, *args):
        thread = threading.Thread(target=func, args=args)
        self.threads.append(thread)
        thread.start()

    def prepare_filename(self, filename):
        return os.path.abspath(os.path.join(self.yaml_dir, filename))