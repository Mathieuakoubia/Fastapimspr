from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


### SCHEMA POUR LES VENDEURS (Resellers)

# Base commune pour les revendeurs (nom, email, prénom)
class ResellerBase(BaseModel):
    name: str
    surname: str 
    email: str


# Schéma utilisé pour la création d'un revendeur (inclut le mot de passe)
class ResellerCreate(ResellerBase):
    password: str  # Ajout du champ `password` uniquement pour la création

# Schéma pour renvoyer les informations d'un revendeur
class Reseller(ResellerBase):
    id: int
    api_key: str
    is_active: bool

    class Config:
        from_attributes = True  # Permet l'utilisation avec SQLAlchemy

class Login(BaseModel):
    email: str
    password: str
### SCHEMA POUR LES CLIENTS (Customers)

# Base commune pour les clients
class CustomerBase(BaseModel):
    name: str
    surname: Optional[str] = None  # Prénom est optionnel pour les clients
    email: str

# Schéma utilisé pour la création d'un client
class CustomerCreate(CustomerBase):
    pass

# Schéma pour renvoyer les informations d'un client
class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


### SCHEMA POUR LES COMMANDES (Orders)

# Base commune pour les commandes
class OrderBase(BaseModel):
    status: str

# Schéma utilisé pour la création d'une commande
class OrderCreate(OrderBase):
    customers_id: int

# Schéma pour renvoyer les informations d'une commande
class Order(OrderBase):
    id: int
    created_at: datetime
    customer: Customer

    class Config:
        from_attributes = True


### SCHEMA POUR LES PRODUITS (Products)

# Base commune pour les produits
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int

# Schéma utilisé pour la création d'un produit
class ProductCreate(ProductBase):
    pass

# Schéma pour renvoyer les informations d'un produit
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


### SCHEMA POUR LES RELATIONS COMMANDES-PRODUITS (OrderProduct)

# Base commune pour lier commandes et produits
class OrderProductBase(BaseModel):
    quantity: int
    price: float

# Schéma utilisé pour la création d'une relation commande-produit
class OrderProductCreate(OrderProductBase):
    order_id: int
    product_id: int

# Schéma pour renvoyer les informations d'une relation commande-produit
class OrderProduct(OrderProductBase):
    order_id: int
    product_id: int
    order: Order
    product: Product

    class Config:
        from_attributes = True
