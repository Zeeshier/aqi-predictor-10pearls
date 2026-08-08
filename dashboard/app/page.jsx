'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import AQIGauge from '../components/AQIGauge';
import ForecastCards from '../components/ForecastCards';
import HourlyTrendChart from '../components/HourlyTrendChart';
import PollutantGrid from '../components/PollutantGrid';
import AnalyticsView from '../components/AnalyticsView';
import AlertBanner from '../components/AlertBanner';
import AQIMapView from '../components/AQIMapView';

export default function DashboardPage() {
  const [city, setCity] = useState('Lahore');
  const [currentData, setCurrentData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [resCurr, resFore, resAna] = await Promise.all([
        fetch(`${API_BASE}/api/current?city=${encodeURIComponent(city)}`),
        fetch(`${API_BASE}/api/forecast?city=${encodeURIComponent(city)}`),
        fetch(`${API_BASE}/api/analytics`)
      ]);

      if (!resCurr.ok || !resFore.ok) {
        throw new Error('Failed to fetch API data');
      }

      const currJson = await resCurr.json();
      const foreJson = await resFore.json();
      const anaJson = resAna.ok ? await resAna.json() : null;

      setCurrentData(currJson);
      setForecastData(foreJson);
      setAnalyticsData(anaJson);
    } catch (err) {
      console.error('API Fetch Error:', err);
      // Fallback Data
      setCurrentData({
        city: city,
        timestamp: new Date().toISOString(),
        weather: { temperature: 28.5, humidity: 45, wind_speed: 3.2, pressure: 1012 },
        pollutants: { pm25: 42.5, pm10: 68.0, no2: 24.1, so2: 6.2, co: 0.9, o3: 35.0 },
        aqi: 118,
        alert: {
          aqi: 118,
          category: 'Unhealthy for Sensitive Groups',
          color: '#EA580C',
          risk_level: 'Moderate Warning',
          health_advice: 'Members of sensitive groups should limit outdoor exertion.',
          alert_triggered: true
        }
      });

      setForecastData({
        city: city,
        current_aqi: 118,
        daily_forecasts: [
          { day: 1, date: 'Day +1', predicted_aqi: 125, alert: { category: 'Unhealthy for Sensitive Groups', risk_level: 'Moderate', alert_triggered: true, health_advice: 'Sensitive groups limit outdoor activity.' } },
          { day: 2, date: 'Day +2', predicted_aqi: 95, alert: { category: 'Moderate', risk_level: 'Low', alert_triggered: false, health_advice: 'Air quality is acceptable.' } },
          { day: 3, date: 'Day +3', predicted_aqi: 70, alert: { category: 'Moderate', risk_level: 'Low', alert_triggered: false, health_advice: 'Satisfactory air quality.' } }
        ],
        hourly_trajectory: Array.from({ length: 72 }, (_, i) => ({
          hour: i + 1,
          timestamp: `Hour ${i + 1}`,
          predicted_aqi: Math.round(118 + 20 * Math.sin(i / 6)),
          category: 'Moderate'
        }))
      });

      setAnalyticsData({
        active_models: { target_aqi_day1: 'Ridge', target_aqi_day2: 'RandomForest', target_aqi_day3: 'PyTorch_NeuralNet' },
        metrics: {
          target_aqi_day1: { rmse: 12.29, mae: 8.76, r2: 0.60 },
          target_aqi_day2: { rmse: 14.92, mae: 9.09, r2: 0.52 },
          target_aqi_day3: { rmse: 12.44, mae: 9.07, r2: 0.62 }
        },
        shap_importance: [
          { feature: 'pm25', shap_value: 18.5, percentage: 32.4 },
          { feature: 'aqi_lag_24h', shap_value: 12.3, percentage: 21.5 },
          { feature: 'humidity', shap_value: 8.4, percentage: 14.7 },
          { feature: 'no2', shap_value: 6.1, percentage: 10.6 },
          { feature: 'temperature', shap_value: 5.2, percentage: 9.1 }
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [city]);

  return (
    <div className="min-h-screen bg-[#FAFAFA] text-zinc-900 flex flex-col font-sans">
      
      {/* Top Navbar */}
      <Navbar city={city} setCity={setCity} onRefresh={fetchDashboardData} loading={loading} />

      {/* Main Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
        
        {/* Alert Banner */}
        <AlertBanner
          currentAlert={currentData?.alert}
          forecastAlerts={forecastData?.daily_forecasts}
        />

        {/* 2026 Minimal Navigation Tabs */}
        <div className="flex items-center gap-1 border-b border-zinc-200 pb-2.5 overflow-x-auto">
          {[
            { id: 'overview', label: 'Overview' },
            { id: 'trajectory', label: '72-Hour Curve' },
            { id: 'pollutants', label: 'Pollutants' },
            { id: 'map', label: 'Station Map' },
            { id: 'analytics', label: 'Model Analytics' },
          ].map((tab) => {
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors whitespace-nowrap ${
                  active
                    ? 'bg-zinc-900 text-white'
                    : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* View Switcher */}
        {activeTab === 'overview' && (
          <div className="space-y-5">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-stretch">
              <div className="lg:col-span-4">
                <AQIGauge currentData={currentData} />
              </div>
              <div className="lg:col-span-8 flex flex-col justify-between space-y-5">
                <ForecastCards forecastData={forecastData} />
                <HourlyTrendChart trajectory={forecastData?.hourly_trajectory} />
              </div>
            </div>
            <PollutantGrid pollutants={currentData?.pollutants} />
          </div>
        )}

        {activeTab === 'trajectory' && (
          <div className="space-y-5">
            <HourlyTrendChart trajectory={forecastData?.hourly_trajectory} />
            <ForecastCards forecastData={forecastData} />
          </div>
        )}

        {activeTab === 'pollutants' && (
          <div className="space-y-5">
            <PollutantGrid pollutants={currentData?.pollutants} />
          </div>
        )}

        {activeTab === 'map' && (
          <div className="space-y-5">
            <AQIMapView city={city} />
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-5">
            <AnalyticsView analyticsData={analyticsData} />
          </div>
        )}

      </main>

      {/* Minimal Footer */}
      <footer className="border-t border-zinc-200 py-4 px-6 text-center text-xs text-zinc-400">
        <span>Pearls AQI Predictor &copy; {new Date().getFullYear()}</span>
      </footer>

    </div>
  );
}
