from dotenv import load_dotenv
import os

load_dotenv()

# App settings:
SECRET_KEY = os.getenv("SECRET_KEY", "abcd")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Db urls:
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")