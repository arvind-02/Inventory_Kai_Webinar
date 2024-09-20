from pydantic import BaseModel, BeforeValidator, validator, Field
from datetime import datetime
from bson import ObjectId as BsonObjectId
from typing import Any, Annotated, Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]
    
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    name: str

    class Config:
        populate_by_name=True
        arbitrary_types_allowed=True 
    

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    price: float
    product_name: str
    quantity: int
    image_path:str
    product_description: str

    class Config:
        populate_by_name=True
        arbitrary_types_allowed=True 

    

class Order(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: Optional[PyObjectId]
    product_id: Optional[PyObjectId]
    quantity: int
    order_time: datetime
    user_name: str
    product_name: str
    product_description: str
    product_price: float
    product_image_path:str

    class Config:
        populate_by_name=True
        arbitrary_types_allowed=True 
    
class OrdersResponse(BaseModel):
    orders: List[Order]
    execution_time: float
    

class RecommendedProduct(BaseModel):
    id: str
    product_name: str
    product_description: str
    image_path: str
    similarity_score: float
    outreach_email: str
    execution_time: float
    


class UserHistory(BaseModel):
    orders_month: int
    quantity_month: int
    spent_month: float

    orders_year: int
    quantity_year: int
    spent_year: float
    execution_time: float

class ProductHistory(BaseModel):
    orders_month: int
    quantity_month: int
    spent_month: float

    orders_year: int
    quantity_year: int
    spent_year: float
    execution_time: float

   

    