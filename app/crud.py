from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets

from . import models
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_reseller_by_email(db: Session, email: str):
    return db.query(models.Reseller).filter(models.Reseller.email == email).first()

def get_reseller_by_api_key(db: Session, api_key: str):
    return db.query(models.Reseller).filter(models.Reseller.api_key == api_key).first()

def create_reseller(db: Session, reseller: schemas.ResellerCreate):
    api_key = secrets.token_urlsafe(32)  # Générer une clé d'autorisation sécurisée
    db_reseller = models.Reseller(
        name=reseller.name,
        email=reseller.email,
        api_key=api_key,
        is_active=True
    )
    db.add(db_reseller)
    db.commit()
    db.refresh(db_reseller)
    return db_reseller


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
