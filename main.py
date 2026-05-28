from fastapi import FastAPI
from database import create_db_and_tables, engine
from services import load_data, set_db
from models.users import User
from models.products import Product
from routers.users import router as users_router
from routers.products import router as products_router


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