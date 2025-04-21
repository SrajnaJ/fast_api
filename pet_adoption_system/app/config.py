import os


# App settings:
SECRET_KEY = os.getenv("SECRET_KEY", "abcd")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Db urls:
DATABASE_URL = os.getenv("DATABASE_URL","mysql+mysqlconnector://root:Abcd%401234@localhost/pet_adoption_db")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "mysql+mysqlconnector://root:Abcd%401234@localhost/test_pet_db")