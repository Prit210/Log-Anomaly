import React, { useEffect, useState } from "react";
import { fetchLogs, fetchStats } from "./api";

function App() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    const interval = setInterval(async () => {
      setLogs(await fetchLogs());
      setStats(await fetchStats());
    }, 10000); // 🔥 10 sec

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>🚀 DeepLog Dashboard</h1>

      <div style={{ display: "flex", gap: 20 }}>
        <div style={card("blue")}>Total: {stats.total}</div>
        <div style={card("red")}>Abnormal: {stats.abnormal}</div>
        <div style={card("green")}>Normal: {stats.normal}</div>
      </div>

      <h3>📜 Logs</h3>
      <table border="1" width="100%">
        <thead>
          <tr>
            <th>Time</th>
            <th>Block</th>
            <th>Event</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={i} style={{
              background: log.event === "SUMMARY" ? "#e0f2fe" : "white"
            }}>
              <td>{log.time}</td>
              <td>{log.block}</td>
              <td>{log.event === "SUMMARY" ? "📊 SUMMARY" : log.event}</td>
              <td style={{
                color: log.status === "ABNORMAL" ? "red" : "green",
                fontWeight: "bold"
              }}>
                {log.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const card = (color) => ({
  padding: 15,
  background: color,
  color: "white",
  borderRadius: 8
});

export default App;