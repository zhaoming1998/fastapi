from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from .config import settings
from psycopg2.extras import RealDictCursor
import time

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<databasename>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# using direct SQL:
'''
while True:
    try:
        conn = psycopg2.connect(host='localhost',dbname='fastapi',user='postgres',password='991230',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection is successful')
        break
    except Exception as error:
        print('Connection to database is failed')
        print('Error is:', error)
        time.sleep(2)
        break
'''
