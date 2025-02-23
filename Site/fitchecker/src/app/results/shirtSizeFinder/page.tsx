'use client';

import { useState } from 'react';

export interface SizeResponse {
    timestamp: string;
    userLogin: string;
    [key: string]: any;  // For other brand size predictions
}

export interface SizeFormData {
    chest: number;
    waist: number;
    shoulder: number;
}

export default function SizePredictionForm() {
    const [formData, setFormData] = useState<SizeFormData>({
        chest: 0,
        waist: 0,
        shoulder: 0,
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<SizeResponse | null>(null);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: parseFloat(value) || 0
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(
                `/api/shirtSizeFinder?chest=${formData.chest}&waist=${formData.waist}&shoulder=${formData.shoulder}`
            );

            if (!response.ok) {
                throw new Error('Failed to get size predictions');
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Something went wrong');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="px-6 py-8">
                    <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">
                        Size Prediction
                    </h2>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {['chest', 'waist', 'shoulder'].map((measurement) => (
                            <div key={measurement}>
                                <label
                                    htmlFor={measurement}
                                    className="block text-sm font-medium text-gray-700 capitalize mb-2"
                                >
                                    {measurement} (cm)
                                </label>
                                <input
                                    type="number"
                                    id={measurement}
                                    name={measurement}
                                    value={formData[measurement as keyof SizeFormData]}
                                    onChange={handleInputChange}
                                    className="block w-full px-4 py-3 rounded-md border border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                    required
                                    min="1"
                                    step="0.1"
                                />
                            </div>
                        ))}

                        <button
                            type="submit"
                            disabled={loading}
                            className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors
                ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
                        >
                            {loading ? 'Predicting...' : 'Predict Size'}
                        </button>
                    </form>

                    {error && (
                        <div className="mt-4 p-4 bg-red-50 rounded-md">
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    {result && (
                        <div className="mt-6 p-4 bg-green-50 rounded-md">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Results</h3>
                            <div className="space-y-2">
                                <p className="text-sm text-gray-600">
                                    Timestamp: {result.timestamp}
                                </p>
                                <p className="text-sm text-gray-600">
                                    User: {result.userLogin}
                                </p>
                                {/* Display brand predictions */}
                                {Object.entries(result).map(([key, value]) => {
                                    if (key !== 'timestamp' && key !== 'userLogin') {
                                        return (
                                            <p key={key} className="text-sm text-gray-800">
                                                <span className="font-medium capitalize">{key}:</span>{' '}
                                                {JSON.stringify(value)}
                                            </p>
                                        );
                                    }
                                    return null;
                                })}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}