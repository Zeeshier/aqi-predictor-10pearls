'use client';

import React from 'react';

export default function ForecastCards({ forecastData }) {
  if (!forecastData || !forecastData.daily_forecasts) return null;

  const getBadgeStyle = (aqi) => {
    if (aqi <= 50) return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (aqi <= 100) return 'bg-amber-50 text-amber-700 border-amber-200';
    if (aqi <= 150) return 'bg-orange-50 text-orange-700 border-orange-200';
    if (aqi <= 200) return 'bg-rose-50 text-rose-700 border-rose-200';
    return 'bg-purple-50 text-purple-700 border-purple-200';
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
      {forecastData.daily_forecasts.map((item) => {
        const alert = item.alert || {};

        return (
          <div
            key={item.day}
            className="clean-card p-4 flex flex-col justify-between"
          >
            {/* Day Header */}
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-zinc-500">
                Day +{item.day} ({item.date})
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getBadgeStyle(item.predicted_aqi)}`}>
                {alert.category}
              </span>
            </div>

            {/* AQI Prediction Number */}
            <div className="my-2 flex items-baseline justify-between">
              <div>
                <span className="text-3xl font-black text-zinc-900 tracking-tight">
                  {item.predicted_aqi}
                </span>
                <span className="text-xs text-zinc-400 font-medium ml-2">AQI</span>
              </div>
            </div>

            {/* Advice Snippet */}
            <p className="text-[11px] text-zinc-500 line-clamp-2 mt-2 leading-relaxed">
              {alert.health_advice}
            </p>
          </div>
        );
      })}
    </div>
  );
}
