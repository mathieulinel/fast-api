from sqlmodel import Field, SQLModel
import datetime

format_string = '%Y-%m-%d %H:%M:%S'

class UserBase(SQLModel):
    username : str | None = Field(default=None)
    email : str | None = Field(default=None)
    role : str | None = Field(default=None)
    active : bool | None = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = 'users'
    id : int | None = Field(default=None, primary_key=True)
    created_at : str = Field(default=datetime.datetime.now(datetime.timezone.utc).strftime(format_string))
    updated_at : str | None = Field(default=None, sa_column_kwargs={"onupdate":datetime.datetime.now(datetime.timezone.utc).strftime(format_string)})

class UserPublic(UserBase):
    id: int
    created_at : str
    updated_at : str | None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    role: str | None = None
    active: bool | None = None