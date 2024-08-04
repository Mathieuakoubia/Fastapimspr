import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = 'mysql+pymysql://admin225:GUmx29225AWS@apimspr2.ctqm0qeikja8.eu-west-3.rds.amazonaws.com:3306/apimsprdb'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
