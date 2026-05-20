from sqlmodel import Field, SQLModel
import datetime

format_string = '%Y-%m-%d %H:%M:%S'

class ProductBase(SQLModel):
    name : str | None = Field(default=None)
    category : str | None = Field(default=None)
    price: float | None = Field(default=None)
    stock: float | None = Field(default=None)
    rating : float | None = Field(default=None)
    review_count: int | None = Field(default=None)
    active : bool | None = Field(default=None)


class Product(ProductBase, table=True):
    __tablename__ = 'products'
    id : int | None = Field(default=None, primary_key=True)
    created_at : str = Field(default=datetime.datetime.now(datetime.timezone.utc).strftime(format_string))
    updated_at : str | None = Field(default=None, sa_column_kwargs={"onupdate":datetime.datetime.now(datetime.timezone.utc).strftime(format_string)})

class ProductPublic(ProductBase):
    id: int
    created_at : str
    updated_at : str | None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name : str | None
    category : str | None
    price: float | None
    stock: float | None
    rating : float | None 
    review_count: int | None 
    active : bool | None 