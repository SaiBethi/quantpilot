import React, { useState } from 'react';

function AIInsights() {
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState(null);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">AI Market Insights</h1>
      
      <div className="card mb-8">
        <h2 className="text-2xl font-semibold mb-4">Stock Analysis</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="ticker" className="block text-sm font-medium text-gray-700 mb-1">
              Stock Ticker
            </label>
            <input
              type="text"
              id="ticker"
              className="input-field"
              placeholder="Enter stock symbol (e.g., AAPL)"
            />
          </div>
          
          <button
            className="btn-primary"
            onClick={() => {
              // TODO: Implement API call to backend
              setLoading(true);
              setTimeout(() => {
                setLoading(false);
                setInsights({
                  recommendation: 'Buy',
                  confidence: 85,
                  analysis: 'Strong technical indicators and positive market sentiment suggest potential upward momentum.'
                });
              }, 1500);
            }}
          >
            Generate Insights
          </button>
        </div>
      </div>

      {loading && (
        <div className="card">
          <p className="text-gray-600">Analyzing market data...</p>
        </div>
      )}

      {insights && !loading && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold">AI Recommendation</h3>
            <span className={`px-3 py-1 rounded-full ${
              insights.recommendation === 'Buy' ? 'bg-green-100 text-green-800' :
              insights.recommendation === 'Sell' ? 'bg-red-100 text-red-800' :
              'bg-yellow-100 text-yellow-800'
            }`}>
              {insights.recommendation}
            </span>
          </div>
          
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-600">Confidence Score</span>
              <span className="font-semibold">{insights.confidence}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${insights.confidence}%` }}
              ></div>
            </div>
          </div>

          <div>
            <h4 className="font-semibold mb-2">Analysis</h4>
            <p className="text-gray-700">{insights.analysis}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AIInsights;