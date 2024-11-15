import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

ARTIFACTS_DIR = os.path.join("artifacts")
LOGS_DIR = "logs"
LOGS_FILE_NAME = "SIDFC.log"


#Gemini Environment Model
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

#AWS S3 Bucket Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET = os.getenv("AWS_BUCKET")


