import React, { useEffect, useState } from 'react';
import MetricsCard from './components/MetricsCard';
import AnomalyAlert from './components/AnomalyAlert';
import HistoricalChart from './components/HistoricalChart';

function App() {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const res = await fetch('http://localhost:5000/monitor');
    const json = await res.json();
    setData(json);
  };

  useEffect(() => {
    fetchData(); // Initial call
    const interval = setInterval(fetchData, 5000); // Repeat every 5s
    return () => clearInterval(interval); // Clean up on unmount
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>🔍 System Monitor Dashboard</h2>
      {data && (
        <>
          <MetricsCard metrics={data} />
          <AnomalyAlert isAnomaly={data.anomaly} />
          <HistoricalChart data={data} />
        </>
      )}
    </div>
  );
}

export default App;
