"use client";

import { api } from "../api.js";
import {useState} from 'react'

export function OrdersList({ orders = [] }) {
  const [recommendations, setRecommendations] = useState({});

  const getRecommendation = async (userName, productId, orderId, productName, productDescription) => {
    if (recommendations[orderId]) {
      setRecommendations(state => ({...state, [orderId]: undefined}))
    } else {
      try {
        const response = await api.get(`recommended/${productId}?user_name=${encodeURIComponent(userName)}&prev_product_name=${encodeURIComponent(productName)}&prev_product_description=${encodeURIComponent(productDescription)}`);
        const recommendation = response.data;
        setRecommendations(state => ({...state, [orderId]: recommendation}))
      } catch (error) {
        console.error("Error fetching recommendation:", error);
      }
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {orders.map((order) => (
        <div key={order._id} className="bg-white shadow-md rounded-lg p-6 ">
          <h2 className="text-xl font-semibold mb-2">Order {order._id}</h2>
          <h2 className="text-xl font-semibold mb-2">{order.user_name}</h2>
          <p className="text-gray-600 mb-2">
            Product: {order.product_name}
          </p>
          <p className="text-gray-600 mb-2">
            Description: {order.product_description}
          </p>
          <img
            src={order.product_image_path}
            alt={order.product_name}
            className="w-full h-32 object-contain rounded-md"
          />
          <p className="text-gray-600 mb-2">Amount: {order.quantity}</p>
          <p className="text-gray-600 mb-2">
            Total Price: ${(order.product_price * order.quantity).toFixed(2)}
          </p>

          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={() => getRecommendation(order.user_name, order.product_id, order._id, order.product_name, order.product_description)}
          >
            {recommendations[order._id]
              ? "Hide Recommendation"
              : "Get Recommendation"}
          </button>
          {recommendations[order._id] && (
            <div className="mt-2">
              <p className="text-gray-600 mb-2">
                Recommended Product: {recommendations[order._id].product_name}
              </p>
              <img
                src={recommendations[order._id].image_path}
                alt={order.product_name}
                className="w-full h-32 object-contain rounded-md"
              />
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
              >
                Get Email

              </button>
              <p className="text-gray-600 mb-2">
                Email: {recommendations[order._id].outreach_email}
              </p>
            </div>
            
          )}
        </div>
      ))}
    </div>
  );
}