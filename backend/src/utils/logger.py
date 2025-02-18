from loguru import logger
from datetime import datetime

date = datetime.now()
year = date.year
month = date.month
day = date.day
logger.add(f"loggers/{day}-{month}-{year}.log", level="INFO")
