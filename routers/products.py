from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from sqlmodel import Session, select
from database import get_session
from models.products import Product, ProductPublic, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/", response_model=ProductPublic)
def create_product(product: ProductCreate, session: SessionDep):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.get("/", response_model=list[ProductPublic])
def read_products(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    category_query: Annotated[str, Query(...)] = None
):
    products = session.exec(select(Product).where(category_query).offset(offset).limit(limit)).all()
    return products

@router.get("/{product_id}", response_model=ProductPublic)
def read_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"msg": f"product id:{product.id}, name: {product.name} has been deleted."}

@router.patch("/{product_id}", response_model=ProductPublic)
def update_product(product_id: int, product: ProductUpdate, session: SessionDep):
    product_db = session.get(Product, product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product.model_dump(exclude_unset=True)
    product_db.sqlmodel_update(product_data)
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db
