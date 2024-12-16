import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

# Détermine l'URL de la base de données en fonction de l'environnement
DATABASE_URL = os.getenv('TEST_DATABASE_URL') if os.getenv('TESTING') == 'true' else os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("La variable d'environnement DATABASE_URL ou TEST_DATABASE_URL est manquante")

print("DATABASE_URL:", DATABASE_URL)  # Affiche la valeur de DATABASE_URL

# Initialise le moteur et la session SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Fournit une session de base de données pour les requêtes FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
