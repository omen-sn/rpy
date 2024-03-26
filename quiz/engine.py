import random
import time
from datetime import datetime
from pathlib import Path
import logging

from quiz.utils.input_reader import InputReader
from quiz.utils.file_writer import FileWriter
from quiz.utils.statistics import Statistics
from quiz.data.question_data import QuestionData
from quiz.config import Config

class Engine:
    def __init__(self):
        try:
            config = Config()
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            self.question_data = QuestionData(yaml_dir=config.yaml_dir)
            answers_filename = f"answers{current_time}.txt" # Приклад імені файлу
            self.writer = FileWriter('a+', answers_filename, answers_dir=config.answers_dir)
            self.statistics = Statistics(self.writer)
            self.input_reader = InputReader()

            user_name = self.input_reader.read(
                welcome_message="Будь ласка, введіть ваше ім'я:",
                error_message="Ім'я не може бути порожнім.",
                validator=lambda input: not input.strip() == ""
            )

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.writer.write(f"Тест розпочато користувачем {user_name} о {current_time}")
        except Exception as e:
            logging.error(f"Помилка під час ініціалізації Engine: {e}")
            raise

    def run(self):
        try:
            start_time = time.time()
            shuffled_questions = self.question_data.collection
            random.shuffle(shuffled_questions)
            for question in shuffled_questions:
                print(question)
                print(question.display_answers())
                value, user_answer = self.get_answer_by_char(question)
                correct_answer = question.question_correct_answer
                self.check(user_answer, correct_answer)
                self.writer.write(f"Question: {question}, Your answer: {user_answer}, Correct answer: {correct_answer}")
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.statistics.print_report()
            print(f"Тест завершено за {elapsed_time:.2f} секунд.")
            self.writer.write(f"Тест завершено о {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logging.error(f"Помилка під час виконання тесту: {e}")
            # Можете додати додаткову логіку для обробки помилки, наприклад, вивести повідомлення користувачу

    def check(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            self.statistics.correct_answer()
        else:
            self.statistics.incorrect_answer()

    def get_answer_by_char(self, question):
        answer = None
        while answer is None:
            char = self.input_reader.read(
                welcome_message="Введіть вашу відповідь (A, B, C, D):",
                error_message="Неправильне введення. Будь ласка, введіть валідну літеру.",
                validator=lambda input: input.upper() in ['A', 'B', 'C', 'D'] and input.strip() != ""
            ).upper()
            answer = question.find_answer_by_char(char)
        return answer, char
