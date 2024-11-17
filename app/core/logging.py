import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure the log directory exists
log_dir = "app/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the level to INFO or DEBUG for detailed logs
logger.setLevel(logging.INFO)

# Create handlers (Console and Rotating File Handler)
console_handler = logging.StreamHandler()  # Logs to console
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "registration.log"), maxBytes=10**6, backupCount=3
)  # 1MB file size limit, 3 backups

# Create formatters and add them to handlers
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
