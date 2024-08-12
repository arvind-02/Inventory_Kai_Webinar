from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
import schemas
import crud
from typing import List
from pymongo.database import Database



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
    return {"message": "Root"}

@app.get("/orders", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Database = Depends(get_db)):
    try:
        orders = crud.get_orders(db, skip=skip, limit=limit)
        return orders

    except SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
@app.get("/recommended/{product_id}", response_model=schemas.RecommendedProduct)
def get_recommended(product_id: str, user_name: str, prev_product_name: str, prev_product_description: str, limit: int = 1, db: Database = Depends(get_db)):
    try:
        result = crud.get_recommended_product(product_id, db)
        email = crud.get_email(prev_product_name, result["product_name"], prev_product_description, result["product_description"], user_name)
        return schemas.RecommendedProduct(id=result["_id"], product_name=result["product_name"],
                                          product_description=result["product_description"], 
                                          image_path=result["image_path"], 
                                          similarity_score=result["similarity_score"], 
                                          outreach_email=email)

    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error occurred")

@app.get("/recommended/{product_id}", response_model=schemas.RecommendedProduct)
def get_email(product_id: str, limit: int = 1, db: Database = Depends(get_db)):
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)