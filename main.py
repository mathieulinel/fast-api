# main.py
from fastapi import FastAPI
from database import create_db_and_tables, engine
from services import load_data
from models.users import User
from models.products import Product
from routers.users import router as users_router
from routers.products import router as products_router
import os
import shutil

DATA_DIR = os.getenv("DATA_DIR", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def set_path(item: str) -> str:
    dest = os.path.join(DATA_DIR, f"{item}.json")
    if not os.path.exists(dest):
        shutil.copy(os.path.join("data", f"{item}.json"), dest)
    return dest

app = FastAPI(title="this is the api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    load_data(set_path("users"), User, engine)
    load_data(set_path("products"), Product, engine)

app.include_router(users_router)
app.include_router(products_router)

@app.get("/")
def root():
    return {"message": "Hello math"}