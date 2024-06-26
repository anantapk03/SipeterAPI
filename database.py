from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL ="mysql+mysqldb://root:capstone@34.101.52.82:3306/sipeter"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency untuk mendapatkan sesi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
