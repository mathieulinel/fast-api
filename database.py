from sqlmodel import Session, SQLModel, create_engine
from services import set_db
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv('DB')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')
db_host = os.getenv('DB_HOST')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

db_url = set_db(db, port=db_port, host=db_host, database=db_name, username=db_username, password=db_password)
## sqlite config specific
# connect_args = {"check_same_thread": False}
engine = create_engine(db_url, echo=True) #, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session