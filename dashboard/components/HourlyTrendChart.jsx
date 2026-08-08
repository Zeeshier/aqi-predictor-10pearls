'use client';

import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-zinc-900 text-white p-2.5 rounded-lg shadow-xl text-xs space-y-0.5">
        <p className="font-semibold">{data.timestamp}</p>
        <p className="text-emerald-400 font-bold">AQI: {data.predicted_aqi}</p>
        <p className="text-[10px] text-zinc-400">{data.category}</p>
      </div>
    );
  }
  return null;
};

export default function HourlyTrendChart({ trajectory }) {
  if (!trajectory || trajectory.length === 0) return null;

  return (
    <div className="clean-panel p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-zinc-900">
            72-Hour AQI Trajectory
          </h3>
          <p className="text-xs text-zinc-400">Predicted hourly AQI curve</p>
        </div>

        {/* Minimal Legend */}
        <div className="flex items-center gap-3 text-[11px] text-zinc-500 font-medium">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Good
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-amber-500"></span> Moderate
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-rose-500"></span> Unhealthy
          </span>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trajectory} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="lightAqiColor" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#18181B" stopOpacity={0.1} />
                <stop offset="95%" stopColor="#18181B" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#F4F4F5" />
            <XAxis
              dataKey="timestamp"
              tickFormatter={(str) => str ? str.split(' ')[1] : ''}
              stroke="#A1A1AA"
              fontSize={11}
              tickLine={false}
            />
            <YAxis stroke="#A1A1AA" fontSize={11} domain={[0, 'auto']} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            
            <ReferenceLine y={50} stroke="#10B981" strokeDasharray="3 3" opacity={0.4} />
            <ReferenceLine y={100} stroke="#F59E0B" strokeDasharray="3 3" opacity={0.4} />
            <ReferenceLine y={150} stroke="#EF4444" strokeDasharray="3 3" opacity={0.4} />
            
            <Area
              type="monotone"
              dataKey="predicted_aqi"
              stroke="#18181B"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#lightAqiColor)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
