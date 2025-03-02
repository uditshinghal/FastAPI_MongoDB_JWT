import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = "243aa093858ddca05b70bca6fb5aa3f9f890dcc306adf3e7b560826853a753c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MONGO_URI = "mongodb://host.docker.internal:27017"
DB_NAME = os.getenv("DB_NAME", "fastapi_db")
