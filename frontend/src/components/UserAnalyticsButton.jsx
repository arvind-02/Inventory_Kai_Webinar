"use client"
import {useState} from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import { api } from "../api"
import ViewUAButton from './ViewUserAnalyticsButton'; 

export default function UserAnalyticsButton({order = {}}){
    const [userAnalytics, setUserAnalytics] = useState(undefined);
    const [loading, setLoading] = useState(false);

    const getUserAnalytics = async (userId) => {
        
        setLoading(true)
        try {
            const response = await api.get(`user_history/${userId}`)
            const user_analytics = response.data
            setUserAnalytics(user_analytics)
        }   catch (error) {
            console.error("Error fetching User Analytics:", error);
        }   finally {
            setLoading(false); // Stop loading
        }
        
    };

    return (
        <div className="flex flex-col items-center space-y-4">
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded  w-full"
                onClick={() => getUserAnalytics(order.user_id)}
            >
                Fetch User Analytics
            </button>
            

            {loading && (
                
                <ClipLoader color={"#09f"} loading={loading} size={24} /> 
                 
            )}

            {userAnalytics && !loading &&(
                
                <ViewUAButton user_analytics = {userAnalytics} name = {order.user_name} />
                
                
            )}

        </div>
    )
}