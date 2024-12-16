from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .Databases import Base
import datetime


class Reseller(Base):
    __tablename__ = "resellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)  # Longueur maximale de 50 caractères
    surname = Column(String(50), index=True)  # Longueur maximale de 50 caractèressurname VARCHAR(50)
    email = Column(String(100), unique=True, index=True)  # Longueur maximale de 100 caractères
    api_key = Column(String(100), unique=True, index=True)  # Longueur maximale de 100 caractères
    is_active = Column(Boolean, default=True)
    password = Column(String(255))


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)  # Longueur maximale de 50 caractères
    surname = Column(String(50))  # Longueur maximale de 50 caractères
    email = Column(String(100), unique=True, index=True)  # Longueur maximale de 100 caractères


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customers_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(20), index=True)  # Longueur maximale de 20 caractères
    
    customer = relationship("Customer")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Longueur maximale de 100 caractères
    description = Column(String(255))  # Longueur maximale de 255 caractères
    price = Column(DECIMAL)
    stock = Column(Integer)


class OrderProduct(Base):
    __tablename__ = "orderproducts"
    
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer)
    price = Column(DECIMAL)

    order = relationship("Order")
    product = relationship("Product")
