'use client';

import React from 'react';
import { AlertCircle, X } from 'lucide-react';

export default function AlertBanner({ currentAlert, forecastAlerts }) {
  const [dismissed, setDismissed] = React.useState(false);

  const activeAlert = currentAlert?.alert_triggered
    ? currentAlert
    : forecastAlerts?.find((a) => a.alert?.alert_triggered)?.alert;

  if (!activeAlert || !activeAlert.alert_triggered || dismissed) {
    return null;
  }

  return (
    <div className="p-3.5 rounded-xl border border-rose-200 bg-rose-50/70 text-rose-900 shadow-sm flex items-center justify-between gap-3">
      <div className="flex items-center gap-2.5">
        <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
        <div className="text-xs">
          <span className="font-bold mr-1.5">{activeAlert.risk_level}:</span>
          <span className="text-rose-800">{activeAlert.health_advice}</span>
        </div>
      </div>

      <button
        onClick={() => setDismissed(true)}
        className="p-1 rounded-md hover:bg-rose-100 text-rose-600 transition-colors"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}
