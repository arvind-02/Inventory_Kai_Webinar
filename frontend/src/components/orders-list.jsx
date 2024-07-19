"use client";

import { api } from "../api.js";
import {useState} from 'react'

export function OrdersList({ orders = [] }) {
  const [recommendations, setRecommendations] = useState({});

  const getRecommendation = async (productId, orderId) => {
    if (recommendations[orderId]) {
      setRecommendations(state => ({...state, [orderId]: undefined}))
    } else {
      try {
        const response = await api.get(`recommended/${productId}`);
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
        <div key={order.id} className="bg-white shadow-md rounded-lg p-6 ">
          <h2 className="text-xl font-semibold mb-2">Order {order.id}</h2>
          <h2 className="text-xl font-semibold mb-2">{order.user.name}</h2>
          <p className="text-gray-600 mb-2">
            Product: {order.product.product_name}
          </p>
          <p className="text-gray-600 mb-2">
            Description: {order.product.product_description}
          </p>
          <img
            src={order.product.image_path}
            alt={order.product.name}
            className="w-full h-32 object-contain rounded-md"
          />
          <p className="text-gray-600 mb-2">Amount: {order.quantity}</p>
          <p className="text-gray-600 mb-2">
            Total Price: ${(order.product.price * order.quantity).toFixed(2)}
          </p>

          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={() => getRecommendation(order.product.id, order.id)}
          >
            {recommendations[order.id]
              ? "Hide Recommendation"
              : "Get Recommendation"}
          </button>
          {recommendations[order.id] && (
            <div className="mt-2">
              <p className="text-gray-600 mb-2">
                Recommended Product: {recommendations[order.id].product_name}
              </p>
              <img
                src={recommendations[order.id].image_path}
                alt={order.product.name}
                className="w-full h-32 object-contain rounded-md"
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}