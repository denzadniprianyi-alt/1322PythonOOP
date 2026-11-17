import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

current_date = datetime.now().strftime("%Y-%m-%d")

logging.info(f"Поточна дата: {current_date}")
