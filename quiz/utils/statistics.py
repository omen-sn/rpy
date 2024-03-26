import logging


class Statistics:
    def __init__(self, writer):
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.writer = writer

    def correct_answer(self):
        self.correct_answers += 1

    def incorrect_answer(self):
        self.incorrect_answers += 1

    def print_report(self):
        try:
            total_questions = self.correct_answers + self.incorrect_answers
            correct_percentage = (self.correct_answers / total_questions * 100) if total_questions > 0 else 0

            report = "Підсумок тесту:\n"
            report += f"Коректні відповіді: {self.correct_answers}\n"
            report += f"Некоректні відповіді: {self.incorrect_answers}\n"
            report += f"Загальна кількість запитань: {total_questions}\n"
            report += f"Процент коректних відповідей: {correct_percentage:.2f}%\n"

            self.writer.write(report)
        except Exception as e:
            logging.error(f"Помилка під час генерації звіту: {e}")
