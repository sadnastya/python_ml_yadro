from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


url = URL.create(
    drivername="postgresql",
    username=os.getenv("USERNAME_POSTGRESQL"),
    password=os.getenv("PASSWORD_POSTGRESQL"),
    host=os.getenv("HOST_POSTGRESQL"),
    port=os.getenv("PORT_POSTGRESQL"),
    database="app"
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
