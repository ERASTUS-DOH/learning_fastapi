import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection url for database.
SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:Me%40Eli24@localhost/fastapi"

# connetion sqlalchemy connection with database.
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# session creator.
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# declarative base class binder.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

while True:
    try:
        conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", password = "Me@Eli24", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!!!!!!!!!!!!!!")
        break
    except Exception as e:
        print("Connection to db failed......")
        print(e)
        time.sleep(2)

