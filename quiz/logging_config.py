import logging
from pathlib import Path

def setup_logging():
    log_filename = Path(__file__).resolve().parent / 'quiz_app.log'
    logging.basicConfig(
        filename=log_filename,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    )
