from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
import schemas
from typing import List
import crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

purchases = [
    {"id": 1, "name": "John Doe", "product": "Laptop", "amount": 1000, "picture":"x", "recommended product": "a"},
    {"id": 2, "name": "Jane Smith", "product": "Phone", "amount": 500, "picture":"y", "recommended product": "b"}, 
    {"id": 3, "name": "Bob Johnson", "product": "Tablet", "amount": 300, "picture":"z", "recommended product": "c"},
]

@app.get("/orders", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        orders = crud.get_orders(db, skip=skip, limit=limit)
        return orders

    except SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)