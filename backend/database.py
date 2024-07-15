from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine_link = os.environ.get("DATABASE_LINK")
engine = create_engine(engine_link)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally: 
        db.close()

def get_engine():
    conn = engine.connect()
    try:
        yield conn
    
    finally: 
        conn.close()
    