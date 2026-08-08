import './globals.css';

export const metadata = {
  title: 'Pearls AQI Predictor',
  description: 'Air Quality Index forecasting application',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="min-h-screen bg-[#FAFAFA] text-zinc-900 antialiased">
        {children}
      </body>
    </html>
  );
}
