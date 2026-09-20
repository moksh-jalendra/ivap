import React, { useEffect, useState } from 'react';

function App() {
  const [status, setStatus] = useState("Connecting to backend...");
  const [detections, setDetections] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [imageSrc, setImageSrc] = useState(null);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || (
      import.meta.env.DEV
        ? 'http://localhost:8000'
        : 'https://ivap-backend.onrender.com'
    );
    const wsUrl = `${apiUrl.replace(/^http/, 'ws')}/api/video/stream`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => setStatus("Connected to Live Feed Stream");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.image) {
          setImageSrc(`data:image/jpeg;base64,${data.image}`);
        }
        if (data.detections) {
          setDetections(data.detections);
        }
        if (data.alerts && data.alerts.length > 0) {
          // Merge new alerts and keep the last 10
          setAlerts(prev => {
            const newAlerts = [...data.alerts, ...prev];
            return newAlerts.slice(0, 10);
          });
        }
      } catch (err) {
        console.error("Failed to parse message", err);
      }
    };
    ws.onclose = () => setStatus("Disconnected from stream");

    return () => ws.close();
  }, []);

  return (
    <div className="min-h-screen p-4 lg:p-8">
      <header className="mb-6 border-b border-gray-700 pb-4">
        <h1 className="text-3xl font-bold text-blue-400">IBVAP Command Center</h1>
        <p className="text-gray-400">Intelligent Border Video Analytics Platform (CPU Optimized)</p>
      </header>
      
      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800 rounded-lg overflow-hidden border border-gray-700 aspect-video flex flex-col items-center justify-center relative">
          
          {imageSrc ? (
            <img src={imageSrc} alt="Live Stream" className="w-full h-full object-contain" />
          ) : (
            <div className="text-gray-500 flex flex-col items-center">
              <svg className="animate-spin h-8 w-8 mb-4 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              [ Waiting for AI Stream... ]
            </div>
          )}
          
          <div className="absolute top-2 left-2 bg-black bg-opacity-60 text-white px-3 py-1 rounded text-sm flex items-center space-x-2">
            <span className={`w-2 h-2 rounded-full ${status.includes('Connected') ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
            <span>{status}</span>
          </div>

          <div className="absolute top-2 right-2 bg-black bg-opacity-60 text-white px-3 py-1 rounded text-sm">
            Objects Tracked: {detections.length}
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700 p-4 flex flex-col h-full max-h-[600px]">
          <h2 className="text-xl font-semibold mb-4 text-red-400 border-b border-gray-700 pb-2 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            Intrusion Alerts (Virtual Fence)
          </h2>
          
          <div className="flex-1 overflow-y-auto">
            {alerts.length === 0 ? (
              <p className="text-gray-400 text-sm italic">No recent intrusions detected in restricted zone.</p>
            ) : (
              <ul className="space-y-3 pr-2">
                {alerts.map((alertText, idx) => (
                  <li key={idx} className="bg-red-900 bg-opacity-40 p-3 rounded text-sm flex justify-between items-center border border-red-800 shadow-sm animate-pulse">
                    <span className="text-red-300 font-bold">{alertText}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
