from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from src.utils.settings import settings


# create the engine 
engine = create_engine(url=settings.DATABASE_URL)
# create session 
SessionLocal = sessionmaker(bind=engine)

def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
    

Base = declarative_base()

   