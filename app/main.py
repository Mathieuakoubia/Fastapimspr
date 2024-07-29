from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models

from . import crud, dependencies
from . import schemas
from .Databases import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/resellers/", response_model=schemas.Reseller)
def create_reseller(reseller: schemas.ResellerCreate, db: Session = Depends(get_db)):
    db_reseller = crud.get_reseller_by_email(db, email=reseller.email)
    if db_reseller:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_reseller(db=db, reseller=reseller)

@app.get("/resellers/me/", response_model=schemas.Reseller)
def read_resellers_me(current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    return current_reseller

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db), current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products