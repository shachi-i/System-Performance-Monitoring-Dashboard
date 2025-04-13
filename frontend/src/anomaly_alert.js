import React from 'react';

function AnomalyAlert({ isAnomaly }) {
  return (
    <div style={{
      background: isAnomaly ? 'red' : 'green',
      color: 'white',
      padding: '10px',
      textAlign: 'center'
    }}>
      {isAnomaly ? '⚠️ Anomaly Detected!' : '✅ All Systems Normal'}
    </div>
  );
}

export default AnomalyAlert;
