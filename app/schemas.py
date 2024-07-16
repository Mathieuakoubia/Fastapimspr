from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ResellerBase(BaseModel):
    name: str
    email: str

class ResellerCreate(ResellerBase):
    pass

class Reseller(ResellerBase):
    id: int
    api_key: str
    is_active: bool

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    surname: Optional[str] = None
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: str

class OrderCreate(OrderBase):
    customers_id: int

class Order(OrderBase):
    id: int
    created_at: datetime
    customer: Customer

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class OrderProductBase(BaseModel):
    quantity: int
    price: float

class OrderProductCreate(OrderProductBase):
    order_id: int
    product_id: int

class OrderProduct(OrderProductBase):
    order_id: int
    product_id: int
    order: Order
    product: Product

    class Config:
        orm_mode = True
