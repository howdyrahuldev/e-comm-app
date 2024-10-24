import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Relative path to the database
DATABASE_URL = "sqlite:///" + os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../products.db")
)


# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
