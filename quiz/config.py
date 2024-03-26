import json
import os
import logging


class ConfigError(Exception):
    pass


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'is_initialized'):
            self.yaml_dir = ""
            self.in_ext = ""
            self.answers_dir = ""
            self.load_config()
            self.is_initialized = True

    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'quiz_config.json')
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            self.yaml_dir = os.path.join(os.path.dirname(__file__), config.get('yaml_dir', ''))
            self.in_ext = config.get('in_ext', '')
            self.answers_dir = os.path.join(os.path.dirname(__file__), config.get('answers_dir', ''))
        except FileNotFoundError:
            logging.error("Файл конфігурації не знайдено.")
            raise ConfigError("Файл конфігурації не знайдено.")
        except json.JSONDecodeError:
            logging.error("Помилка при читанні JSON файлу конфігурації.")
            raise ConfigError("Помилка при читанні JSON файлу конфігурації.")
        except Exception as e:
            logging.error(f"Несподівана помилка: {str(e)}")
            raise ConfigError(f"Несподівана помилка: {str(e)}")

    def print_config(self):
        print("Конфігурація Quiz:")
        print(f"yaml_dir: {self.yaml_dir}")
        print(f"in_ext: {self.in_ext}")
        print(f"answers_dir: {self.answers_dir}")


# Тепер, при спробі створити новий інстанс Config, буде повернуто той самий інстанс:
config1 = Config()
config2 = Config()
assert config1 is config2  # True
