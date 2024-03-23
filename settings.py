from dotenv import find_dotenv, load_dotenv
import os

find_dotenv()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'
