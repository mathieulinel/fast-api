from sqlmodel import Session, insert, text
from sqlalchemy import URL
import json
import os

def set_db(dialect, port=None, host="", database="test.db", username="admin", password="admin"):
    if not database.endswith(".db") and dialect != 'postgres':
            database = f"{database}.db"
    if database.endswith(".db") and dialect == 'postgres':
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
        case "postgres":
            return URL.create(
                    drivername="postgresql+psycopg2",
                    username=username,
                    password=password,
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
            session.execute(text(f"SELECT setval(pg_get_serial_sequence('{table.__tablename__}', 'id'), MAX(id)) FROM {table.__tablename__}"))