import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 900000, // 15 minutes for complex multi-agent research queries
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

  // Execute research with SSE streaming progress updates
  streamResearch: async (researchData, onProgress) => {
    const url = `${API_BASE_URL}/research/stream`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(researchData),
    });

    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(errorBody || `Stream request failed: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let finalResult = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Parse SSE lines from the buffer
      const lines = buffer.split('\n');
      // Keep the last potentially-incomplete line in the buffer
      buffer = lines.pop();

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith('data:')) continue;

        try {
          const event = JSON.parse(trimmed.slice(5).trim());
          if (event.status === 'done' && event.result) {
            finalResult = event.result;
          }
          if (onProgress) {
            onProgress(event);
          }
        } catch (e) {
          console.warn('Failed to parse SSE event:', trimmed, e);
        }
      }
    }

    if (!finalResult) {
      throw new Error('Stream ended without a final result');
    }
    return finalResult;
  },
};

export default apiService;
