from models import Order

orders = [
        Order(order_time="2022-06-15 12:30:00", quantity=1, product_id=product_ids['Laptop'], user_id=users[0].id),
        Order(order_time="2023-01-20 15:45:00", quantity=2, product_id=product_ids['Desk Lamp'], user_id=users[1].id),
        Order(order_time="2021-12-10 09:10:00", quantity=1, product_id=product_ids['Smartphone'], user_id=users[2].id),
        Order(order_time="2023-03-22 18:05:00", quantity=3, product_id=product_ids['Bracelet'], user_id=users[3].id),
        Order(order_time="2022-11-05 13:55:00", quantity=2, product_id=product_ids['Sunglasses'], user_id=users[4].id),
        Order(order_time="2023-05-12 11:20:00", quantity=1, product_id=product_ids['Backpack'], user_id=users[5].id),
        Order(order_time="2022-09-08 14:00:00", quantity=2, product_id=product_ids['Water Bottle'], user_id=users[6].id),
        Order(order_time="2023-04-18 16:30:00", quantity=1, product_id=product_ids['Blender'], user_id=users[7].id),
        Order(order_time="2022-08-25 10:15:00", quantity=3, product_id=product_ids['Sofa'], user_id=users[8].id),
        Order(order_time="2023-02-28 09:00:00", quantity=2, product_id=product_ids['Toaster'], user_id=users[9].id)
    ]