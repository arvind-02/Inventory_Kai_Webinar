"use client"
import { api } from "../api.js";
import  OrdersList  from "../components/OrdersList";
import  HomeBar  from "../components/HomeBar";
import {useState, useEffect} from 'react'
import ClipLoader from "react-spinners/ClipLoader";

export default function Home() {
  const [retrievedResponse, setRetrievedResponse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Simulate data fetching with a delay
      const response = await api.get("/orders");
      setRetrievedResponse(response)
      
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="bg-blue-600 text-white p-6 shadow-md mb-4 rounded-xl">
          <h1 className="text-2xl font-bold text-center">SingleStore ECommerce Dashboard</h1>
        </div>
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <ClipLoader color={"#09f"} loading={loading} size={200} />
          </div>
        ) : (
          retrievedResponse && (
            <>
              <OrdersList orders={retrievedResponse.data.orders} />
              
            </>
          )
        )}
      </div>
    </div>
  );
}
