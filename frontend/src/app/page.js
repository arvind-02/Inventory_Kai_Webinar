'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get('http://localhost:8000/orders', {withCredentials: true,});
        setOrders(response.data);
      } catch (error) {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error('Error response:', error.response.data);
          console.error('Error status:', error.response.status);
          console.error('Error headers:', error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // http.ClientRequest in Node.js
          console.error('Error request:', error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error('Error message:', error.message);
        }
        console.error('Error config:', error.config);
        
      }
      console.log(orders)
    };

    fetchOrders();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Orders</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {orders.map((order) => (
          <div key={order.id} className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">Order {order.id}</h2>
            <h2 className="text-xl font-semibold mb-2">{order.user.name}</h2>
            <p className="text-gray-600 mb-2">Product: {order.product.product_name}</p>
            <img src={order.product.image_path} alt={order.product.name} className="w-full h-32 object-cover rounded-md" />
            <p className="text-gray-600 mb-2">Amount: {order.quantity}</p>
            <p className="text-gray-600 mb-2">Total Price: ${(order.product.price * order.quantity).toFixed(2)}</p>
            <p className="text-gray-600 mb-2">Recommended Product: {"recommended product"}</p>
            
          </div>
        ))}
      </div>
    </div>
  );
}
