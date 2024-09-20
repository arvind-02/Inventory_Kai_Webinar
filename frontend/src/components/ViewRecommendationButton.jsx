"use client"
import {useState} from 'react'

export default function ViewRecommendationButton({rec_info = {}, prev_product = ""}){
    const [viewingRec, setViewingRec] = useState(null);

    return (
        <div className="w-full">
            <button
                className="w-full bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => setViewingRec(rec_info)}
            >
                View Recommendation
            </button>
            
            {viewingRec && (
                <div className="fixed inset-0 flex items-center justify-center z-50">
                    <div className="absolute inset-0 bg-black opacity-50"></div>
                    <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto z-10">
                        <h2 className="text-xl font-semibold mb-4">Recommendation for {prev_product}</h2>
                        <div className="bg-gray-100 p-4 rounded">
                            <p className="text-gray-600 mb-2">
                                <b>Recommended Product:</b> {rec_info.product_name} <br/><br/>
                                <b>Product ID:</b> {rec_info.id} <br/><br/>
                                <b>Description:</b> {rec_info.product_description}

                            </p>

                            <p className="text-gray-600">
                                <br/><br/>
                                <b>Query Execution Time:</b> {rec_info.execution_time.toFixed(3)} seconds
                                
                            </p>
                        </div>
                        <button
                            className="bg-red-500 text-white px-4 py-2 rounded mt-4"
                            onClick={() => setViewingRec(null)}
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}

        </div>


    )
}