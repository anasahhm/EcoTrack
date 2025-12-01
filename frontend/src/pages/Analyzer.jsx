import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { calculateImpact } from '../services/api';

const Analyzer = () => {
  const [formData, setFormData] = useState({
    transport_method: 'car',
    transport_km: 0,
    electricity_kwh: 0,
    water_liters: 0,
    diet_type: 'mixed',
    waste_kg: 0,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await calculateImpact({
        ...formData,
        transport_km: parseFloat(formData.transport_km),
        electricity_kwh: parseFloat(formData.electricity_kwh),
        water_liters: parseFloat(formData.water_liters),
        waste_kg: parseFloat(formData.waste_kg),
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Calculation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getRatingColor = (rating) => {
    const colors = {
      Excellent: 'text-green-600',
      Good: 'text-blue-600',
      Moderate: 'text-yellow-600',
      Poor: 'text-orange-600',
      Critical: 'text-red-600',
    };
    return colors[rating] || 'text-gray-600';
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Environmental Impact Analyzer</h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Transport Method
              </label>
              <select
                name="transport_method"
                value={formData.transport_method}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
              >
                <option value="car">Car</option>
                <option value="bus">Bus</option>
                <option value="bike">Bike</option>
                <option value="walk">Walk</option>
                <option value="ev">Electric Vehicle</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Distance Traveled (km)
              </label>
              <input
                type="number"
                name="transport_km"
                min="0"
                step="0.1"
                value={formData.transport_km}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Electricity Usage (kWh)
              </label>
              <input
                type="number"
                name="electricity_kwh"
                min="0"
                step="0.1"
                value={formData.electricity_kwh}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Water Usage (liters)
              </label>
              <input
                type="number"
                name="water_liters"
                min="0"
                step="1"
                value={formData.water_liters}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Diet Type
              </label>
              <select
                name="diet_type"
                value={formData.diet_type}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
              >
                <option value="veg">Vegetarian</option>
                <option value="mixed">Mixed</option>
                <option value="heavy_meat">Heavy Meat</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Waste Generated (kg)
              </label>
              <input
                type="number"
                name="waste_kg"
                min="0"
                step="0.1"
                value={formData.waste_kg}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary hover:bg-secondary text-white py-3 rounded-md font-semibold disabled:opacity-50"
          >
            {loading ? 'Calculating...' : 'Calculate Impact'}
          </button>
        </form>
      </div>

      {result && (
        <div className="bg-white rounded-lg shadow-md p-6">
<h2 className="text-2xl font-bold mb-6">Your Environmental Impact</h2>
 <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">Carbon Score</p>
          <p className="text-2xl font-bold text-blue-600">{result.carbon_score} kg CO₂</p>
        </div>
        <div className="bg-cyan-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">Water Score</p>
          <p className="text-2xl font-bold text-cyan-600">{result.water_score} L</p>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">Energy Score</p>
          <p className="text-2xl font-bold text-yellow-600">{result.energy_score} kWh</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">Waste Score</p>
          <p className="text-2xl font-bold text-gray-600">{result.waste_score} kg</p>
        </div>
      </div>

      <div className="mb-6">
        <p className="text-lg font-semibold mb-2">Overall Rating</p>
        <p className={`text-3xl font-bold ${getRatingColor(result.overall_rating)}`}>
          {result.overall_rating}
        </p>
      </div>
       {result.ai_analysis && (
      <div className="mb-6 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6">
      <div className="flex items-start">
      <span className="text-3xl mr-3">🤖</span>
      <div>
        <p className="text-sm font-semibold text-purple-700 mb-2">
          AI-Powered Analysis
        </p>
        <p className="text-gray-700 leading-relaxed">
          {result.ai_analysis}
        </p>
      </div>
    </div>
  </div>
)}

      <div>
        <p className="text-lg font-semibold mb-3">Personalized Tips</p>
        <ul className="space-y-2">
          {result.tips.map((tip, index) => (
            <li key={index} className="flex items-start">
              <span className="text-primary mr-2">✓</span>
              <span className="text-gray-700">{tip}</span>
            </li>
          ))}
        </ul>
      </div>

      <button
        onClick={() => navigate('/dashboard')}
        className="mt-6 w-full bg-primary hover:bg-secondary text-white py-2 rounded-md font-semibold"
      >
        View Dashboard
      </button>
    </div>
  )}
</div>
);
};
export default Analyzer;