import logging
from datetime import datetime
import os
import colorlog

log_format = "%(log_color)s%(levelname)s:%(reset)s     %(message)s"

current_date = datetime.now().strftime("%d-%m-%y")
start_time = datetime.now().strftime("%H-%M-%S")

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

log_file_path = f"{log_dir}/{current_date}_{start_time}.log"

console_handler = colorlog.StreamHandler()
console_handler.setFormatter(colorlog.ColoredFormatter(log_format))

file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.INFO)
