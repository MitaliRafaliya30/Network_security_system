import logging
import os
from datetime import datetime

#generates a timestamp in the format MM_DD_YYYY_HH_MM_SS, ensuring each log file has a unique name.
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#os.getcwd(): Gets the current working directory.
#os.path.join(os.getcwd(), "logs", LOG_FILE): Creates a path where logs will be stored, inside a logs folder.
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

#ensures that the "logs" directory and subdirectories are created if they don't already exist.
#exist_ok=True prevents errors if the directory already exists.
os.makedirs(logs_path,exist_ok=True)

#contains the absolute path to the log file.
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH, #filename=LOG_FILE_PATH → Specifies where log messages will be saved.
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO, #  Logs all messages with level INFO or higher.
)