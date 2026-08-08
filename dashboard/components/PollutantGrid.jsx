'use client';

import React from 'react';

export default function PollutantGrid({ pollutants }) {
  if (!pollutants) return null;

  const items = [
    { name: 'PM2.5', label: 'Fine Particles', val: pollutants.pm25, unit: 'µg/m³', limit: 12.0 },
    { name: 'PM10', label: 'Coarse Dust', val: pollutants.pm10, unit: 'µg/m³', limit: 54.0 },
    { name: 'NO2', label: 'Nitrogen Dioxide', val: pollutants.no2, unit: 'µg/m³', limit: 53.0 },
    { name: 'O3', label: 'Ozone', val: pollutants.o3, unit: 'µg/m³', limit: 70.0 },
    { name: 'SO2', label: 'Sulfur Dioxide', val: pollutants.so2, unit: 'µg/m³', limit: 35.0 },
    { name: 'CO', label: 'Carbon Monoxide', val: pollutants.co, unit: 'mg/m³', limit: 4.4 }
  ];

  return (
    <div className="clean-panel p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-zinc-900">
            Pollutant Breakdown
          </h3>
          <p className="text-xs text-zinc-400">Live contaminant metrics</p>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
        {items.map((item) => {
          const ratio = Math.min(100, (item.val / item.limit) * 100);
          const isHigh = item.val > item.limit;

          return (
            <div key={item.name} className="clean-card p-3.5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold mb-1">
                  <span>{item.name}</span>
                  <span className={isHigh ? 'text-rose-600 font-bold' : 'text-emerald-600'}>
                    {isHigh ? 'High' : 'Normal'}
                  </span>
                </div>
                <div className="my-1">
                  <span className="text-xl font-black text-zinc-900">{item.val}</span>
                  <span className="text-[10px] text-zinc-400 ml-1 font-medium">{item.unit}</span>
                </div>
              </div>

              {/* Minimal Progress Bar */}
              <div className="mt-3">
                <div className="h-1 w-full bg-zinc-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${
                      isHigh ? 'bg-rose-500' : 'bg-zinc-800'
                    }`}
                    style={{ width: `${ratio}%` }}
                  ></div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
