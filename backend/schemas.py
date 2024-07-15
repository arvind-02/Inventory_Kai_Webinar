from pydantic import BaseModel, conint
from datetime import datetime
from typing import List, Optional, ForwardRef

OrderRef = ForwardRef('Order')
ProductRef = ForwardRef('Product')
UserRef = ForwardRef('User')

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