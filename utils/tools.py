from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
def get_engine(use_memory=True):
    if use_memory:
        return create_engine('sqlite:///:memory:',echo=False)
    else:
        return create_engine('sqlite:///concerts.db',echo=False)
engine = get_engine(use_memory=False)
SessionLocal = sessionmaker(bind=engine)
#create the tables
def create_db():
    Base.metadata.create_all(engine)