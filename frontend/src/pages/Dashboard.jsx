import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHistory } from '../services/api';
import ScoreCard from '../components/ScoreCard';
import TrendChart from '../components/TrendChart';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await getHistory(1, 7);
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  const latestLog = data?.data[0];
  const logs = data?.data || [];

  // Prepare chart data
  const carbonData = logs.reverse().map((log) => log.carbon_score);
  const waterData = logs.map((log) => log.water_score);
  const energyData = logs.map((log) => log.energy_score);
  const labels = logs.map((log, index) => `Day ${index + 1}`);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={() => navigate('/analyzer')}
          className="bg-primary hover:bg-secondary text-white px-6 py-2 rounded-md font-semibold"
        >
          New Analysis
        </button>
      </div>

      {latestLog ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <ScoreCard
              title="Carbon Footprint"
              value={latestLog.carbon_score}
              unit="kg CO₂"
              icon="🌍"
              color="text-blue-600"
            />
            <ScoreCard
              title="Water Usage"
              value={latestLog.water_score}
              unit="L"
              icon="💧"
              color="text-cyan-600"
            />
            <ScoreCard
              title="Energy Score"
              value={latestLog.energy_score}
              unit="kWh"
              icon="⚡"
              color="text-yellow-600"
            />
            <ScoreCard
              title="Waste Generated"
              value={latestLog.waste_score}
              unit="kg"
              icon="♻️"
              color="text-gray-600"
            />
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-xl font-bold mb-4">Overall Rating</h2>
            <p className="text-3xl font-bold text-primary mb-4">{latestLog.overall_rating}</p>
            <div>
              <h3 className="font-semibold mb-2">Today's Tips:</h3>
              <ul className="space-y-1">
                {latestLog.tips.map((tip, index) => (
                  <li key={index} className="text-gray-700">
                    • {tip}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {logs.length > 1 && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              <TrendChart
                title="Carbon Footprint Trend"
                labels={labels}
                data={carbonData}
                color="rgb(59, 130, 246)"
              />
              <TrendChart
                title="Water Usage Trend"
                labels={labels}
                data={waterData}
                color="rgb(6, 182, 212)"
              />
              <TrendChart
                title="Energy Usage Trend"
                labels={labels}
                data={energyData}
                color="rgb(251, 191, 36)"
              />
            </div>
          )}

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Recent Logs</h2>
            <div className="space-y-3">
              {logs.slice(0, 5).reverse().map((log) => (
                <div key={log.id} className="border-l-4 border-primary pl-4 py-2">
                  <p className="font-semibold">{log.overall_rating}</p>
                  <p className="text-sm text-gray-600">
                    Carbon: {log.carbon_score} kg CO₂ | Water: {log.water_score} L
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(log.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
            <button
              onClick={() => navigate('/history')}
              className="mt-4 text-primary hover:text-secondary font-semibold"
            >
              View All History →
            </button>
          </div>
        </>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <p className="text-xl text-gray-600 mb-4">No data yet!</p>
          <p className="text-gray-500 mb-6">Start tracking your environmental impact today.</p>
          <button
            onClick={() => navigate('/analyzer')}
            className="bg-primary hover:bg-secondary text-white px-8 py-3 rounded-md font-semibold"
          >
            Create First Analysis
          </button>
        </div>
      )}
    </div>
  );
};

export default Dashboard;