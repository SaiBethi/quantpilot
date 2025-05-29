import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // TODO: Implement API call to Streamlit backend
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Stock Analysis Dashboard</h1>
      
      <div className="card mb-8">
        <form onSubmit={handleSubmit} className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-[200px]">
            <label htmlFor="ticker" className="block text-sm font-medium text-gray-700 mb-1">
              Stock Ticker
            </label>
            <input
              type="text"
              id="ticker"
              className="input-field"
              placeholder="e.g., AAPL"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              required
            />
          </div>
          
          <div className="flex-1 min-w-[200px]">
            <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-1">
              Start Date
            </label>
            <input
              type="date"
              id="startDate"
              className="input-field"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
            />
          </div>
          
          <div className="flex-1 min-w-[200px]">
            <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-1">
              End Date
            </label>
            <input
              type="date"
              id="endDate"
              className="input-field"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              required
            />
          </div>
          
          <div className="flex items-end w-full sm:w-auto">
            <button
              type="submit"
              className="btn-primary w-full sm:w-auto"
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Analyze Stock'}
            </button>
          </div>
        </form>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-2xl font-semibold mb-4">Price Chart</h2>
          <div className="h-[400px] flex items-center justify-center bg-gray-50 rounded">
            <p className="text-gray-500">Select a stock to view price data</p>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold mb-4">RSI Indicator</h2>
          <div className="h-[400px] flex items-center justify-center bg-gray-50 rounded">
            <p className="text-gray-500">Select a stock to view RSI data</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;