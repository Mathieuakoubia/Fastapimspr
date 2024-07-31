import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Utiliser 'host.docker.internal' pour permettre au conteneur Docker d'accéder à MySQL sur l'hôte
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@host.docker.internal:3306/ApiMspr')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
