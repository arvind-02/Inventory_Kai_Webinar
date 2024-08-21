import RecommendationButton from "./RecommendationButton"

export default function OrderCard({order = {}}){
    return (
        <div key={order._id} className="bg-white shadow-md rounded-lg p-6">
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

            <RecommendationButton order = {order} />
        </div>


    )
}