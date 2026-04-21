const API = "http://127.0.0.1:8000";

export const fetchLogs = async () => {
  const res = await fetch(`${API}/logs`);
  return res.json();
};

export const fetchStats = async () => {
  const res = await fetch(`${API}/stats`);
  return res.json();
};