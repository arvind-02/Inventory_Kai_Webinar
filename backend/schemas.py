from pydantic import BaseModel, BeforeValidator, validator, Field
from datetime import datetime
from bson import ObjectId as BsonObjectId
from typing import Any, Annotated, Optional

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
    
    
    

class RecommendedProduct(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    product_name: str
    product_description: str
    image_path: str
    similarity_score: float
    outreach_email: str

    