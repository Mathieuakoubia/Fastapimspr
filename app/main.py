import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware


from . import models
from . import crud, dependencies
from . import schemas
from .Databases import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Clé secrète et algorithme pour le token JWT
SECRET_KEY = "votre_cle_secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("Application démarrée.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application arrêtée proprement.")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(reseller: schemas.Login, db: Session = Depends(get_db)):
    """
    Route pour authentifier un utilisateur en JSON.
    """
    db_reseller = crud.authenticate_reseller(db, reseller.email, reseller.password)
    if not db_reseller:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Créer le token JWT
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": db_reseller.email, "exp": expire}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/resellers/", response_model=schemas.Reseller)
def create_reseller(reseller: schemas.ResellerCreate, db: Session = Depends(get_db)):
    db_reseller = crud.get_reseller_by_email(db, email=reseller.email)
    if db_reseller:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_reseller(db=db, reseller=reseller)

@app.get("/resellers/", response_model=List[schemas.Reseller])
def get_all_resellers(db: Session = Depends(get_db)):
    """Récupérer tous les revendeurs."""
    return db.query(models.Reseller).all()


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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

@app.delete("/resellers/{reseller_id}", status_code=204)
def delete_reseller(reseller_id: int, db: Session = Depends(get_db)):
    """
    Supprime un revendeur en fonction de son ID.
    """
    success = crud.delete_reseller(db, reseller_id)
    if not success:
        raise HTTPException(status_code=404, detail="Revendeur introuvable")
    return {"detail": "Revendeur supprimé avec succès"}


@app.put("/resellers/{reseller_id}", response_model=schemas.Reseller)
def update_reseller(reseller_id: int, reseller_update: schemas.ResellerCreate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un revendeur.
    """
    db_reseller = crud.update_reseller(db, reseller_id, reseller_update)
    if not db_reseller:
        raise HTTPException(status_code=404, detail="Revendeur introuvable")
    return db_reseller


@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int,
    customer_update: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller),
):
    db_customer = crud.update_customer(db, customer_id, customer_update)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return db_customer



@app.delete("/orders/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller),
):
    success = crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return {"detail": "Commande supprimée avec succès"}



@app.delete("/orders/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller),
):
    """
    Supprime une commande par ID.
    """
    success = crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return {"detail": "Commande supprimée avec succès"}



@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(
    order_id: int,
    order_update: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller),
):
    """
    Met à jour une commande en fonction de son ID.
    """
    db_order = crud.update_order(db, order_id, order_update)
    if not db_order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return db_order



@app.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller),
):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return {"detail": "Produit supprimé avec succès"}


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_reseller: schemas.Reseller = Depends(dependencies.get_current_reseller),
):
    db_product = crud.update_product(db, product_id, product_update)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return db_product


