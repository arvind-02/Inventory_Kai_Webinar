"use client"
import {useState} from 'react'
import { api } from "../api"
import ViewPAButton from './ViewProductAnalyticsButton'; 
import ClipLoader from "react-spinners/ClipLoader";

export default function ProductAnalyticsButton({order = {}}){
    const [productAnalytics, setProductAnalytics] = useState(undefined);
    const [loading, setLoading] = useState(false);
    

    const getProductAnalytics = async (productId) => {
        
        setLoading(true)
        try {
            const response = await api.get(`product_history/${productId}`)
            const product_analytics = response.data
            console.log(product_analytics)
            setProductAnalytics(product_analytics)
        }   catch (error) {
            console.error("Error fetching Product Analytics:", error);
        }   finally {
            setLoading(false); // Stop loading
        }
    };

    return (
        <div className="flex flex-col items-center space-y-4">
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => getProductAnalytics(order.product_id)}
            >
                Fetch Product Analytics
            </button>

            {loading && (
                
                <ClipLoader color={"#09f"} loading={loading} size={24} /> 
                 
            )}
            {productAnalytics && !loading &&(
                
                <ViewPAButton product_analytics = {productAnalytics} name = {order.product_name} />
                
                
            )}

        </div>
    )
}