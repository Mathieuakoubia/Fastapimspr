from Databases import Base, engine

# Supprime toutes les tables définies dans vos modèles SQLAlchemy
print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

# Recrée toutes les tables définies dans vos modèles SQLAlchemy
print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("Database reset completed.")
