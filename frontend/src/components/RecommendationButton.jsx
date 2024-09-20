"use client"
import {useState} from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import EmailButton  from "./EmailButton";
import { api } from "../api"
import ViewRecommendationButton from './ViewRecommendationButton';

export default function RecommendationButton({order = {}}){
    const [recommendation, setRecommendation] = useState(undefined);
    const [loading, setLoading] = useState(false);

    const getRecommendation = async (userName, productId, productName, productDescription) => {
        
        
      setLoading(true)
      try {
        const response = await api.get(`recommended/${productId}?user_name=${encodeURIComponent(userName)}&prev_product_name=${encodeURIComponent(productName)}&prev_product_description=${encodeURIComponent(productDescription)}`);
        const recommendation = response.data;
        setRecommendation(recommendation)
      } catch (error) {
        console.error("Error fetching recommendation:", error);
      } finally {
        setLoading(false); // Stop loading
      }
        
    };
    return (
        <div className="flex flex-col items-center space-y-4">
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded w-full"
                onClick={() => getRecommendation(order.user_name, order.product_id, order.product_name, order.product_description)}
            >
                Fetch Recommendation
            </button>

            {loading && (
                
               <ClipLoader color={"#09f"} loading={loading} size={24} /> 
                
            )}

            {recommendation && !loading &&(
              <>
                <ViewRecommendationButton rec_info = {recommendation} prev_product={order.product_name}/>
                <EmailButton outreach_email = {recommendation.outreach_email}/>
              </>

            )}


        </div>
    );
}