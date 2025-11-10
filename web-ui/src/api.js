// api.js
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function sendCodeForReview(code) {
  try {
    const res = await axios.post(`${API_URL}/review`, { code }, { timeout: 20000 });
    return { ok: true, data: res.data };
  } catch (err) {
    const message = err?.response?.data?.detail || err.message || 'Unknown error';
    return { ok: false, error: message };
  }
}