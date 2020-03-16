import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = 'secret'
JWT_ACCESS_TOKEN_EXPIRES = 2 * 60 * 1000
JWT_REFRESH_TOKEN_EXPIRES = 30 * 60 * 1000
SQLALCHEMY_ECHO = True
SQLALCHEMY_DB_URI = os.getenv('SQLALCHEMY_DB_URI') or f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'


DISTRICTS_TREE_MAX_DEEP = 10
