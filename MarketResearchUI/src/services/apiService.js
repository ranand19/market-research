import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for complex research queries
});

// API service methods
const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  // Get available research types
  getResearchTypes: async () => {
    try {
      const response = await apiClient.get('/research/types');
      return response.data.research_types;
    } catch (error) {
      console.error('Failed to fetch research types:', error);
      throw error;
    }
  },

  // Get available tools
  getTools: async () => {
    try {
      const response = await apiClient.get('/tools/list');
      return response.data.tools;
    } catch (error) {
      console.error('Failed to fetch tools:', error);
      throw error;
    }
  },

  // Execute research request
  executeResearch: async (researchData) => {
    try {
      const response = await apiClient.post('/research/execute', researchData);
      return response.data;
    } catch (error) {
      console.error('Research execution failed:', error);
      throw error;
    }
  },
};

export default apiService;
