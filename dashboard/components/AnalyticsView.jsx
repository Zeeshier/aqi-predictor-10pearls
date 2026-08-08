'use client';

import React from 'react';

export default function AnalyticsView({ analyticsData }) {
  if (!analyticsData) return null;

  const metrics = analyticsData.metrics || {};
  const activeModels = analyticsData.active_models || {};
  const shapImportance = analyticsData.shap_importance || [];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
      
      {/* SHAP Feature Importance */}
      <div className="clean-panel p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-zinc-900">
              SHAP Feature Importance
            </h3>
            <p className="text-xs text-zinc-400">Explainable AI feature weights</p>
          </div>
        </div>

        <div className="space-y-3 mt-4">
          {shapImportance.slice(0, 7).map((item) => (
            <div key={item.feature} className="text-xs">
              <div className="flex justify-between text-zinc-700 font-medium mb-1">
                <span className="font-mono text-zinc-900">{item.feature}</span>
                <span className="text-zinc-500">{item.percentage}%</span>
              </div>
              <div className="h-1.5 w-full bg-zinc-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-zinc-900 rounded-full transition-all duration-300"
                  style={{ width: `${Math.max(5, item.percentage)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Model Benchmark Table */}
      <div className="clean-panel p-5 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-zinc-900">
                Model Evaluation Benchmark
              </h3>
              <p className="text-xs text-zinc-400">Synced with Hopsworks Model Registry</p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-zinc-100 text-zinc-700 border border-zinc-200">
              Hopsworks Sync
            </span>
          </div>

          <div className="overflow-x-auto mt-2">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="text-zinc-400 border-b border-zinc-100 pb-2">
                  <th className="py-2 font-semibold">Horizon</th>
                  <th className="py-2 font-semibold">Optimal Model</th>
                  <th className="py-2 font-semibold">RMSE</th>
                  <th className="py-2 font-semibold">MAE</th>
                  <th className="py-2 font-semibold">R²</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 font-medium">
                {Object.keys(metrics).map((target) => {
                  const m = metrics[target];
                  const name = activeModels[target] || 'RandomForest';

                  return (
                    <tr key={target} className="hover:bg-zinc-50">
                      <td className="py-2.5 font-bold text-zinc-900 uppercase">
                        {target.replace('target_aqi_', '')}
                      </td>
                      <td className="py-2.5 text-zinc-800 font-semibold">
                        {name}
                      </td>
                      <td className="py-2.5 text-zinc-600">{m.rmse}</td>
                      <td className="py-2.5 text-zinc-600">{m.mae}</td>
                      <td className="py-2.5 text-zinc-900 font-bold">{m.r2}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </div>
  );
}
