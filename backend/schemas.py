from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    name: str

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    price: float
    product_name: str
    quantity: int
    image_path:str
    product_description: str

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    
    quantity: int
    order_time: datetime
    user: User
    product: Product
    
    class Config:
        orm_mode = True

class RecommendedProduct(BaseModel):
    id: int
    product_name: str
    product_description: str
    image_path: str
    similarity_score: float

    class Config:
        from_attributes = True