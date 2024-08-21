import { api } from "../api.js";
import  OrdersList  from "../components/OrdersList";

export default async function Home() {
  let orders = [];

  try {
    const response = await api.get("/orders");
    orders = response.data
  } catch (error) {
    console.error(error);
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Orders</h1>
      <OrdersList orders={orders} />
    </div>
  );
}
