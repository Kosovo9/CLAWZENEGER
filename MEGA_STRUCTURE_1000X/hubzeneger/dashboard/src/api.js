
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
const API_KEY = process.env.REACT_APP_API_KEY || 'default-key-change-me';

const api = axios.create({
    baseURL: API_BASE,
    headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    },
});

export const getStats = () => api.get('/stats');
export const getLeads = () => api.get('/leads');
export const getFunnels = () => api.get('/funnels');
export const getAgentsStatus = () => api.get('/agents/status');
export const runAgentTask = (agentName, payload = {}) => api.post(`/agents/${agentName}/run`, payload);

export default api;
