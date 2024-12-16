from sqlalchemy.orm import Session
from passlib.context import CryptContext

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import qrcode
import os
import secrets

from . import models
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_reseller_by_email(db: Session, email: str):
    return db.query(models.Reseller).filter(models.Reseller.email == email).first()


def get_reseller_by_api_key(db: Session, api_key: str):
    return db.query(models.Reseller).filter(models.Reseller.api_key == api_key).first()


def is_api_key_unique(db: Session, api_key: str) -> bool:
    """
    Vérifie si une clé API est unique dans la base de données.
    """
    return not db.query(models.Reseller).filter(models.Reseller.api_key == api_key).first()


def create_reseller(db: Session, reseller: schemas.ResellerCreate):
    # Générer une clé API unique
    while True:
        api_key = secrets.token_urlsafe(32)  # Génère une clé API aléatoire
        if is_api_key_unique(db, api_key):  # Vérifie si elle est unique
            break

    # Hacher le mot de passe pour le stocker de manière sécurisée
    hashed_password = pwd_context.hash(reseller.password)

    # Créer le nouvel utilisateur (revendeur)
    db_reseller = models.Reseller(
        name=reseller.name,
        surname=reseller.surname,  # Nouveau champ
        email=reseller.email,
        password=hashed_password,  # Mot de passe haché
        api_key=api_key,
        is_active=True
    )  # <- Parenthèse fermante ajoutée ici

    # Générer un QR Code pour la clé API
    qr_data = f"API_KEY: {api_key}"
    qr_path = f"qrcodes/{db_reseller.email}.png"
    os.makedirs("qrcodes", exist_ok=True)  # Créer le dossier s'il n'existe pas
    qr = qrcode.make(qr_data)
    qr.save(qr_path)

    # Envoyer l'e-mail avec le QR Code
    send_email_with_qrcode(db_reseller.email, qr_path)

    db.add(db_reseller)
    db.commit()
    db.refresh(db_reseller)
    return db_reseller


def send_email_with_qrcode(to_email: str, qr_code_path: str):
    from_email = "matheothedon@gmail.com"
    password = "gopu zgei jvjy msrh"
    subject = "Votre QR Code pour l'authentification"

    # Configurer le message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    body = "Veuillez scanner ce QR Code pour vous connecter à l'application."
    message.attach(MIMEText(body, 'plain'))

    # Joindre le QR Code
    with open(qr_code_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename=qr_code.png")
        message.attach(part)

    # Envoyer l'e-mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(message)
        server.quit()
        print(f"E-mail envoyé à {to_email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

def authenticate_reseller(db: Session, email: str, password: str):
    """
    Vérifie si l'email et le mot de passe correspondent à un utilisateur existant.
    """
    db_reseller = db.query(models.Reseller).filter(models.Reseller.email == email).first()
    if not db_reseller:
        return None  # L'utilisateur n'existe pas
    if not pwd_context.verify(password, db_reseller.password):
        return None  # Mot de passe incorrect
    return db_reseller  # Retourne l'utilisateur s'il est authentifié


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_order_product(db: Session, order_product: schemas.OrderProductCreate):
    db_order_product = models.OrderProduct(**order_product.dict())
    db.add(db_order_product)
    db.commit()
    db.refresh(db_order_product)
    return db_order_product
# Reseller
def delete_reseller(db: Session, reseller_id: int) -> bool:
    db_reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not db_reseller:
        return False
    db.delete(db_reseller)
    db.commit()
    return True


def update_reseller(db: Session, reseller_id: int, reseller_update: schemas.ResellerCreate):
    db_reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not db_reseller:
        return None
    for key, value in reseller_update.dict().items():
        setattr(db_reseller, key, value)
    db.commit()
    db.refresh(db_reseller)
    return db_reseller


# Customer
def delete_customer(db: Session, customer_id: int) -> bool:
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True


def update_customer(db: Session, customer_id: int, customer_update: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        return None
    for key, value in customer_update.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# Order
def delete_order(db: Session, order_id: int) -> bool:
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True


def update_order(db: Session, order_id: int, order_update: schemas.OrderCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return None
    for key, value in order_update.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


# Product
def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product
