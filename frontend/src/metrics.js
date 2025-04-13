import React from 'react';

function MetricsCard({ metrics }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', margin: '10px' }}>
      <h3>📈 Live Metrics</h3>
      <p>CPU Usage: {metrics.cpu_usage}%</p>
      <p>Memory Usage: {metrics.memory_usage}%</p>
      <p>Disk I/O: {metrics.disk_io}</p>
    </div>
  );
}

export default MetricsCard;
