"use client"
import {useState} from 'react'

export default function EmailButton({outreach_email = ""}){
    const [viewingEmail, setViewingEmail] = useState(null);

    return (
        <div>
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => setViewingEmail(outreach_email)}
            >
                View Outreach Email
            </button>

            {viewingEmail && (
                <div className="fixed inset-0 flex items-center justify-center z-50">
                    <div className="absolute inset-0 bg-black opacity-50"></div>
                    <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto z-10">
                        <h2 className="text-xl font-semibold mb-4">Outreach Email</h2>
                        <div className="bg-gray-100 p-4 rounded">
                            <p dangerouslySetInnerHTML={{__html: viewingEmail}}></p>
                        </div>
                        <button
                            className="bg-red-500 text-white px-4 py-2 rounded mt-4"
                            onClick={() => setViewingEmail(null)}
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}

        </div>


    )
}