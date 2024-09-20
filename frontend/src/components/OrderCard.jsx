"use client"
import RecommendationButton from "./RecommendationButton"
import UserAnalyticsButton from "./UserAnalyticsButton"
import ProductAnalyticsButton from "./ProductAnalyticsButton"

export default function OrderCard({order = {}}){
    return (
        <div key={order._id} className="bg-white shadow-lg rounded-lg p-6 border-2 border-gray-400">
            <h2 className="text-xl font-bold mb-2">Order {order._id}</h2>
            <h2 className="text-xl font-bold mb-2">{order.user_name}</h2>
            <h2 className="text-xl font-bold mb-2">
              {new Date(order.order_time).toLocaleString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric', 
                hour: 'numeric', 
                minute: 'numeric', 
                second: 'numeric',
                hour12: true // This makes it display as AM/PM. Set to false for 24-hour format.
              })}
            </h2>
            <p className="text-gray-600 mb-2">
              <span className="font-bold">Product:</span> {order.product_name}
            </p>
            <p className="text-gray-600 mb-8">
            <span className="font-bold">Description:</span> {order.product_description}
            </p>
            <img
              src={order.product_image_path}
              alt={order.product_name}
              className="w-full h-32 object-contain rounded-md justify-center mb-8"
            />
            <p className="text-gray-600 mb-2">
            <span className="font-bold">Amount:</span> {order.quantity}
              </p>
            <p className="text-gray-600 mb-8">
            <span className="font-bold">Total Price:</span> ${(order.product_price * order.quantity).toFixed(2)}
            </p>

            <div className="flex flex-row gap-4 mt-4 justify-center w-full">
                <RecommendationButton order={order}  />
                <UserAnalyticsButton order={order} />
                <ProductAnalyticsButton order={order} />
            </div>
        </div>


    )
}