from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, BigInteger, Text, LargeBinary
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_singlestoredb import VECTOR
from sqlalchemy.types import TypeEngine
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    orders = relationship("Order", 
                          back_populates="user",
                          primaryjoin="User.id == foreign(Order.user_id)")
    

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(50))
    product_description = Column(Text)
    price = Column(Float)
    quantity = Column(Integer)
    image_path = Column(String(255))
    
    orders = relationship("Order", 
                          back_populates="product",
                          primaryjoin="Product.id == foreign(Order.product_id)")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_time = Column(DateTime(timezone=True))
    product_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    product = relationship("Product", 
                           back_populates="orders",
                           primaryjoin="foreign(Order.product_id) == Product.id")
    user = relationship("User", 
                        back_populates="orders",
                        primaryjoin="foreign(Order.user_id) == User.id")
    

