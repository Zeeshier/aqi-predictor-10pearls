'use client';

import React from 'react';
import { RefreshCw, MapPin } from 'lucide-react';

export default function Navbar({ city, setCity, onRefresh, loading }) {
  const cities = [
    'Lahore',
    'Karachi',
    'Islamabad',
    'Rawalpindi',
    'Peshawar',
    'Quetta',
    'Multan',
    'Faisalabad',
    'Sialkot',
    'Gujranwala',
    'Hyderabad'
  ];

  return (
    <header className="bg-white border-b border-zinc-200 sticky top-0 z-50 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Header */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-zinc-900 text-white flex items-center justify-center font-bold text-xs">
            AQI
          </div>
          <div>
            <h1 className="text-base font-bold text-zinc-900 tracking-tight flex items-center gap-2">
              Pearls Predictor
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-zinc-100 text-zinc-600 border border-zinc-200">
                Pakistan
              </span>
            </h1>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5">
          {/* City Picker */}
          <div className="relative flex items-center">
            <MapPin className="w-3.5 h-3.5 absolute left-3 text-zinc-400 pointer-events-none" />
            <select
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="bg-zinc-50 text-zinc-900 text-xs font-semibold rounded-lg pl-8 pr-7 py-2 border border-zinc-200 focus:outline-none focus:border-zinc-400 cursor-pointer appearance-none"
            >
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
            <span className="pointer-events-none absolute right-2.5 text-zinc-400 text-[10px]">▼</span>
          </div>

          {/* Refresh */}
          <button
            onClick={onRefresh}
            disabled={loading}
            className="p-2 rounded-lg bg-zinc-100 hover:bg-zinc-200 text-zinc-700 transition-colors border border-zinc-200 active:scale-95 disabled:opacity-50"
            title="Refresh Data"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-zinc-900' : ''}`} />
          </button>
        </div>

      </div>
    </header>
  );
}
