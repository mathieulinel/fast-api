from sqlmodel import Session, insert
from sqlalchemy import URL
import json
import os

def set_db(dialect, port=None, host="", database="test.db", username="mathieulinel"):
    if not database.endswith(".db") and dialect != 'postgresql':
            database = f"{database}.db"
    if database.endswith(".db") and dialect == 'postgresql':
            database = os.path.splitext(database)[0]
    match dialect:
        case "sqlite":
            return URL.create(
                    drivername="sqlite",
                    host=host,
                    database=database
                )
        case "mysql":
            return URL.create(
                    drivername="mysql+pymysql",
                    host=host or "localhost",
                    database=database,
                    port=port or 3306
                )
        case "postgresql":
            return URL.create(
                    drivername="postgresql+psycopg2",
                    username=username,
                    # password=password,
                    host=host or "localhost",
                    database=database,
                    port=port or 5432
                )
        case "memory":
            pass    
        case _:
            raise ValueError(f"Unsupported dialect: {dialect}")

def load_data(filepath: str, table, engine):
    with open(filepath, 'r') as file:
        data = json.load(file)
        with Session(bind=engine) as session:
            session.execute(insert(table), data)
            session.commit()