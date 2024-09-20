from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
import schemas
import crud
from typing import List
from pymongo.database import Database
import time




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

@app.get("/orders", response_model=schemas.OrdersResponse)
def get_orders(skip: int = 0, limit: int = 50, db: Database = Depends(get_db)):
    try:
        start_time = time.time()
        orders = crud.get_orders(db, skip=skip, limit=limit)
        execution_time = time.time() - start_time
        print(f"execution time: {execution_time}")
        return schemas.OrdersResponse(orders=orders, execution_time=execution_time)

    except SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    
@app.get("/recommended/{product_id}", response_model=schemas.RecommendedProduct)
def get_recommended(product_id: str, user_name: str, prev_product_name: str, prev_product_description: str, limit: int = 1, db: Database = Depends(get_db)):
    try:
        start_time = time.time()
        result = crud.get_recommended_product(product_id, db)
        email = crud.get_email(prev_product_name, result["product_name"], prev_product_description, result["product_description"], user_name)
        execution_time = time.time() - start_time
        return schemas.RecommendedProduct(id=result["_id"], product_name=result["product_name"],
                                          product_description=result["product_description"], 
                                          image_path=result["image_path"], 
                                          similarity_score=result["similarity_score"], 
                                          outreach_email=email, 
                                          execution_time=execution_time)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e)


@app.get("/user_history/{user_id}", response_model=schemas.UserHistory)
def get_user_history(user_id:str, db: Database = Depends(get_db)):
    try:
        start_time = time.time()
        customer_month_info = crud.get_user_month_history(user_id, db)
        

        customer_year_info = crud.get_user_year_history(user_id, db)
        execution_time = time.time() - start_time
        return schemas.UserHistory(orders_month=customer_month_info['total_orders_last_month'],
                                   quantity_month=customer_month_info['total_quantity_ordered_last_month'],
                                   spent_month=customer_month_info['total_amount_spent_last_month'],
                                   orders_year=customer_year_info['total_orders_last_year'],
                                   quantity_year=customer_year_info['total_quantity_ordered_last_year'],
                                   spent_year=customer_year_info['total_amount_spent_last_year'],
                                   execution_time=execution_time)
    except Exception as e:
        print(e)
        
        raise HTTPException(status_code=500, detail="Database error occurred")
    

@app.get("/product_history/{product_id}", response_model=schemas.UserHistory)
def get_product_history(product_id:str, db: Database = Depends(get_db)):
    try:
        start_time = time.time()
        product_month_info = crud.get_product_month_history(product_id, db)
        

        product_year_info = crud.get_product_year_history(product_id, db)
        execution_time = time.time() - start_time
        return schemas.ProductHistory(orders_month=product_month_info['total_orders_last_month'],
                                   quantity_month=product_month_info['total_quantity_ordered_last_month'],
                                   spent_month=product_month_info['total_amount_spent_last_month'],
                                   orders_year=product_year_info['total_orders_last_year'],
                                   quantity_year=product_year_info['total_quantity_ordered_last_year'],
                                   spent_year=product_year_info['total_amount_spent_last_year'],
                                   execution_time=execution_time)
    except Exception as e:
        print(e)
        
        raise HTTPException(status_code=500, detail="Database error occurred")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)