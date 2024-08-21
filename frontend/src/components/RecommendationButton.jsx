"use client"
import {useState} from 'react'
import EmailButton  from "./EmailButton";
import { api } from "../api"

export default function RecommendationButton({order = {}}){
    const [recommendation, setRecommendation] = useState(undefined);

    const getRecommendation = async (userName, productId, productName, productDescription) => {
        
        if (recommendation) {
          setRecommendation(undefined)
        } else {
          try {
            const response = await api.get(`recommended/${productId}?user_name=${encodeURIComponent(userName)}&prev_product_name=${encodeURIComponent(productName)}&prev_product_description=${encodeURIComponent(productDescription)}`);
            const recommendation = response.data;
            setRecommendation(recommendation)
          } catch (error) {
            console.error("Error fetching recommendation:", error);
          }
        }
    };
    return (
        <div>
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => getRecommendation(order.user_name, order.product_id, order.product_name, order.product_description)}
            >
                {recommendation ? "Hide Recommendation" : "Get Recommendation"}
            </button>
            {recommendation && (
                <div className="mt-2">
                <p className="text-gray-600 mb-2">
                    Recommended Product: {recommendation.product_name}
                </p>
                <img
                    src={recommendation.image_path}
                    alt={recommendation.product_name}
                    className="w-full h-32 object-contain rounded-md mb-4"
                />
                <EmailButton outreach_email = {recommendation.outreach_email}/>
                </div>
            )}


        </div>
    );
}