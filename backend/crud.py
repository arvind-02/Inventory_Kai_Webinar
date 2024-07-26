from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection
from models import Order, Product, User
from sqlalchemy import text

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def get_recommended_product(product_id: int, connection: Connection):
    query = text("""
    WITH reference_product AS (
        SELECT description_embedding
        FROM products
        WHERE id = :product_id
    )
    SELECT p.id, p.product_name, p.product_description, p.image_path, 
           p.description_embedding <*> (SELECT description_embedding FROM reference_product) AS similarity_score
    FROM products p
    WHERE p.id != :product_id
    ORDER BY similarity_score DESC
    LIMIT 1
    """)

    values = {"product_id": product_id}
    result = connection.execute(query, values).fetchone()

    return (result.id, result.product_name, result.product_description, result.image_path, result.similarity_score)

    

