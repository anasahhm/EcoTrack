import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

const Home = () => {
  const { isAuthenticated } = useSelector((state) => state.auth);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Track Your Environmental Impact
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            EcoTrack helps you understand and reduce your carbon footprint through
            daily habit tracking, personalized insights, and actionable recommendations.
          </p>
          <div className="flex justify-center space-x-4">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="bg-primary hover:bg-secondary text-white px-8 py-3 rounded-lg text-lg font-semibold transition"
              >
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link
                  to="/signup"
                  className="bg-primary hover:bg-secondary text-white px-8 py-3 rounded-lg text-lg font-semibold transition"
                >
                  Get Started
                </Link>
                <Link
                  to="/login"
                  className="bg-white hover:bg-gray-100 text-primary border-2 border-primary px-8 py-3 rounded-lg text-lg font-semibold transition"
                >
                  Login
                </Link>
              </>
            )}
          </div>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">Track Daily Habits</h3>
            <p className="text-gray-600">
              Monitor your transportation, energy usage, diet, and waste generation
              with our easy-to-use impact analyzer.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-xl font-bold mb-2">Visualize Trends</h3>
            <p className="text-gray-600">
              See your environmental impact over time with interactive charts
              and comprehensive analytics.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-4xl mb-4">💡</div>
            <h3 className="text-xl font-bold mb-2">Get Personalized Tips</h3>
            <p className="text-gray-600">
              Receive tailored recommendations to reduce your carbon footprint
              based on your lifestyle patterns.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;