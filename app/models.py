from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .Databases import Base
import datetime


class Reseller(Base):
    __tablename__ = "resellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String)
    email = Column(String, unique=True, index=True)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customers_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, index=True)
    
    customer = relationship("Customer")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
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
