import json
import random
import logging
import yaml


class Question:
    def __init__(self, raw_text, raw_answers):
        self.question_body = raw_text
        self.question_answers = {}
        self.question_correct_answer = None
        self.load_answers(raw_answers)

    def display_answers(self):
        """Відображення відповідей у зручному форматі."""
        return '\n'.join([f"{char}. {answer}" for char, answer in self.question_answers.items()])

    def __str__(self):
        return self.question_body

    def to_dict(self):
        """Представлення об'єкта у вигляді словника."""
        return {
            "question_body": self.question_body,
            "question_correct_answer": self.question_correct_answer,
            "question_answers": self.question_answers,
        }

    def to_json(self):
        """Представлення об'єкта у вигляді JSON."""
        return json.dumps(self.to_dict(), indent=2)

    def to_yaml(self):
        """Представлення об'єкта у вигляді YAML."""
        return yaml.dump(self.to_dict(), default_flow_style=False)

    def load_answers(self, raw_answers):
        """Завантаження та обробка відповідей."""
        correct_answer = next((a for a in raw_answers if a.startswith('$')), None)
        if correct_answer:
            correct_answer = correct_answer[1:].strip()
        else:
            logging.warning("Жодна з відповідей не позначена як правильна. Призначено першу відповідь.")
            correct_answer = raw_answers[0].strip()

        shuffled_answers = [a[1:].strip() if a.startswith('$') else a.strip() for a in raw_answers]
        random.shuffle(shuffled_answers)
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        self.question_answers = {letters[i]: answer for i, answer in enumerate(shuffled_answers)}
        self.question_correct_answer = letters[shuffled_answers.index(correct_answer)]

    def find_answer_by_char(self, char):
        """Пошук відповіді за символом."""
        return self.question_answers.get(char)

# Додатково: Щоб використовувати yaml.dump, потрібно встановити PyYAML
# pip install PyYAML