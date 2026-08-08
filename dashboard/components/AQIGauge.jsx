'use client';

import React from 'react';

export default function AQIGauge({ currentData }) {
  if (!currentData) return null;

  const aqi = currentData.aqi || 0;
  const alert = currentData.alert || {};
  const weather = currentData.weather || {};

  // Status color mapping for clean solid badges
  const getBadgeStyle = (category) => {
    if (aqi <= 50) return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (aqi <= 100) return 'bg-amber-50 text-amber-700 border-amber-200';
    if (aqi <= 150) return 'bg-orange-50 text-orange-700 border-orange-200';
    if (aqi <= 200) return 'bg-rose-50 text-rose-700 border-rose-200';
    return 'bg-purple-50 text-purple-700 border-purple-200';
  };

  return (
    <div className="clean-panel p-6 flex flex-col justify-between h-full">
      
      {/* Panel Header */}
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">
          Current Air Quality
        </span>
        <span className="text-[11px] font-mono text-zinc-400">
          {currentData.city}
        </span>
      </div>

      {/* Main AQI Number Display */}
      <div className="my-6 text-center">
        <div className="text-6xl font-black text-zinc-900 tracking-tight">
          {aqi}
        </div>
        <div className="text-xs font-medium text-zinc-400 mt-1 uppercase tracking-widest">
          US EPA Index
        </div>

        {/* Status Pill Badge */}
        <div className="mt-4">
          <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold border ${getBadgeStyle(alert.category)}`}>
            {alert.category || 'Good'}
          </span>
        </div>
      </div>

      {/* Health Advice Line */}
      <p className="text-xs text-zinc-600 text-center line-clamp-2 px-2 font-normal leading-relaxed">
        {alert.health_advice}
      </p>

      {/* Weather Strip */}
      <div className="grid grid-cols-3 gap-2 mt-6 pt-4 border-t border-zinc-100 text-center">
        <div>
          <span className="text-[10px] text-zinc-400 uppercase font-semibold block">Temp</span>
          <span className="text-xs font-bold text-zinc-800">{weather.temperature}°C</span>
        </div>
        <div>
          <span className="text-[10px] text-zinc-400 uppercase font-semibold block">Humidity</span>
          <span className="text-xs font-bold text-zinc-800">{weather.humidity}%</span>
        </div>
        <div>
          <span className="text-[10px] text-zinc-400 uppercase font-semibold block">Wind</span>
          <span className="text-xs font-bold text-zinc-800">{weather.wind_speed} m/s</span>
        </div>
      </div>

    </div>
  );
}
