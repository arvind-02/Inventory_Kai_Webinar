from sqlalchemy.orm import Session
import schemas
from models import Order, Product, User

from sqlalchemy import desc

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


from database import SessionLocal
db = SessionLocal()
orders = get_orders(db)
for order in orders:
        user = order.user
        attributes = [attr for attr in dir(order) if not attr.startswith('_') and not callable(getattr(order, attr))]
        for attr in attributes:
            print(f"  {attr}: {getattr(order, attr)}")
        print(f"Order ID: {order.id}, User ID: {order.user_id}, Product ID: {order.product_id}, Quantity: {order.quantity}")
