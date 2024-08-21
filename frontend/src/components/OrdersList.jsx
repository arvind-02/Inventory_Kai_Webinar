import { api } from "../api.js";
import OrderCard  from "./OrderCard";

export default function OrdersList({orders = []}) {
  
  return (
    <div className="relative">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {orders.map((order) => <OrderCard key={order._id} order={order}/>)}
      </div>
    </div>
  )
}