import logging
import sys

# Get the logger instance
logger = logging.getLogger("DevMentor")

# Set logger level to INFO. Then it will handle info, warning, error and critical messages
logger.setLevel(logging.INFO)

# Create handler to to write logs to the console
handler = logging.StreamHandler(sys.stdout)

# Create a formatter and add it to the handler
# This format includes the timestamp, logger name, level, and message
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


# Add the handler to the logger
# This check prevents adding duplicate handlers if the script is reloaded
if not logger.handlers:
    logger.addHandler(handler)
