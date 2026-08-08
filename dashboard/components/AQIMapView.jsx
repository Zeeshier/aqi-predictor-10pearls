'use client';

import React from 'react';

export default function AQIMapView({ city }) {
  const cityCoords = {
    Lahore: { lat: 31.5204, lon: 74.3587, zoom: 11 },
    Karachi: { lat: 24.8607, lon: 67.0011, zoom: 11 },
    Islamabad: { lat: 33.6844, lon: 73.0479, zoom: 11 },
    Rawalpindi: { lat: 33.5651, lon: 73.0169, zoom: 11 },
    Peshawar: { lat: 34.0151, lon: 71.5249, zoom: 11 },
    Quetta: { lat: 30.1798, lon: 66.9750, zoom: 11 },
    Multan: { lat: 30.1575, lon: 71.5249, zoom: 11 },
    Faisalabad: { lat: 31.4504, lon: 73.1350, zoom: 11 },
    Sialkot: { lat: 32.4945, lon: 74.5229, zoom: 11 },
    Gujranwala: { lat: 32.1877, lon: 74.1945, zoom: 11 },
    Hyderabad: { lat: 25.3960, lon: 68.3578, zoom: 11 }
  };

  const currentConfig = cityCoords[city] || { lat: 30.3753, lon: 69.3451, zoom: 6 };

  return (
    <div className="clean-panel p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-zinc-900">
            Live AQI Station Map
          </h3>
          <p className="text-xs text-zinc-400">{city}, Pakistan</p>
        </div>

        <span className="text-xs text-zinc-500 font-mono bg-zinc-100 px-2.5 py-1 rounded-md border border-zinc-200">
          {currentConfig.lat}, {currentConfig.lon}
        </span>
      </div>

      <div className="relative w-full h-[450px] rounded-lg overflow-hidden border border-zinc-200 bg-zinc-100">
        <iframe
          src={`https://aqicn.org/map/world/#@${currentConfig.lat},${currentConfig.lon},${currentConfig.zoom}z`}
          className="w-full h-full border-0"
          title={`AQICN Map - ${city}`}
          loading="lazy"
        ></iframe>
      </div>
    </div>
  );
}
