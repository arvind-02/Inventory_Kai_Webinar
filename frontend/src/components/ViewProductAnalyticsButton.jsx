"use client"
import {useState} from 'react'

export default function ViewPAButton({product_analytics = {}, name = ""}){
    const [viewingPA, setViewingPA] = useState(null);

    return (
        <div className="w-full">
            <button
                className="w-full bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => setViewingPA(product_analytics)}
            >
                View Product Analytics
            </button>
            
            {viewingPA && (
                <div className="fixed inset-0 flex items-center justify-center z-50">
                    <div className="absolute inset-0 bg-black opacity-50"></div>
                    <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto z-10">
                        <h2 className="text-xl font-semibold mb-4">Product Analytics for {name}</h2>
                        <div className="bg-gray-100 p-4 rounded">
                            <p className="text-gray-600 mb-2">
                                <b>Total Orders Last Year:</b> {product_analytics.orders_year} <br />
                                <b>Total Quantity Ordered Last Year:</b> {product_analytics.quantity_year} <br />
                                <b>Total Amount Purchased Last Year:</b> ${product_analytics.spent_year.toFixed(2)} <br />
                                <br />
                                <b>Total Orders Last Month:</b> {product_analytics.orders_month} <br />
                                <b>Total Quantity Ordered Last Month:</b> {product_analytics.quantity_month} <br />
                                <b>Total Amount Purchased Last Month:</b> ${product_analytics.spent_month.toFixed(2)} <br />
                                <br />
                                <b>Query Execution Time:</b> {product_analytics.execution_time.toFixed(3)} seconds

                            </p>
                            
                        </div>
                        <button
                            className="bg-red-500 text-white px-4 py-2 rounded mt-4"
                            onClick={() => setViewingPA(null)}
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}

        </div>


    )
}