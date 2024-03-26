import logging


class InputReader:
    def read(self, welcome_message=None, validator=None, error_message=None, process=None):
        if welcome_message:
            print(welcome_message)
        try:
            user_input = input().strip()
            if process:
                user_input = process(user_input)
        except Exception as e:
            logging.error(f"Помилка при обробці вводу: {e}")
            raise e

        while validator and not validator(user_input):
            if error_message:
                print(error_message)
            try:
                user_input = input().strip()
                if process:
                    user_input = process(user_input)
            except Exception as e:
                logging.error(f"Помилка при повторному введенні: {e}")
                raise e

        return user_input


# Приклад використання
if __name__ == "__main__":
    from quiz.logging_config import setup_logging

    # Виклик setup_logging() на початку програми для ініціалізації налаштувань логування
    # Або це може бути зроблено в основному скрипті вашої програми
    setup_logging()

    reader = InputReader()


    def is_integer(input_str):
        return input_str.isdigit()


    def to_integer(input_str):
        return int(input_str)


    try:
        input_number = reader.read(
            welcome_message="Будь ласка, введіть ціле число:",
            validator=is_integer,
            error_message="Це не ціле число. Спробуйте ще раз:",
            process=to_integer
        )
        print(f"Введене число: {input_number}")
    except Exception as e:
        logging.error(f"Виникла помилка під час читання вводу: {e}")
