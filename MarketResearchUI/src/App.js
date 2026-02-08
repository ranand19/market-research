import React, { useState, useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Snackbar, Alert } from '@mui/material';
import theme from './styles/theme';
import ResearchInputScreen from './components/ResearchInputScreen';
import ResearchResultsScreen from './components/ResearchResultsScreen';
import apiService from './services/apiService';

function App() {
  const [currentScreen, setCurrentScreen] = useState('input');
  const [researchResults, setResearchResults] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const health = await apiService.healthCheck();
      if (health.status === 'healthy') {
        setBackendStatus('connected');
        setSnackbar({
          open: true,
          message: '✓ Connected to AI backend successfully',
          severity: 'success',
        });
      }
    } catch (error) {
      setBackendStatus('disconnected');
      setSnackbar({
        open: true,
        message: '⚠ Backend not available. Please start the API server.',
        severity: 'warning',
      });
    }
  };

  const handleResearchComplete = (results) => {
    setResearchResults(results);
    setCurrentScreen('results');
    setSnackbar({
      open: true,
      message: '✓ Research completed successfully!',
      severity: 'success',
    });
  };

  const handleNewResearch = () => {
    setCurrentScreen('input');
    setResearchResults(null);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          backgroundColor: '#f5f7fa',
          backgroundImage: `
            linear-gradient(rgba(0, 61, 165, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 61, 165, 0.02) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
        }}
      >
        {/* Albertsons Brand Header */}
        <Box
          sx={{
            background: 'linear-gradient(90deg, #003da5 0%, #0066cc 100%)',
            color: 'white',
            py: 1.5,
            px: 3,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                fontSize: '1.5rem',
                fontWeight: 700,
                letterSpacing: '-0.5px',
              }}
            >
              ALBERTSONS COMPANIES
            </Box>
            <Box
              sx={{
                fontSize: '0.875rem',
                backgroundColor: 'rgba(255,255,255,0.2)',
                px: 2,
                py: 0.5,
                borderRadius: '12px',
              }}
            >
              Market Intelligence Platform
            </Box>
          </Box>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              fontSize: '0.875rem',
            }}
          >
            <Box
              sx={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                backgroundColor: backendStatus === 'connected' ? '#4caf50' : '#ff9800',
              }}
            />
            {backendStatus === 'connected' ? 'AI Backend Active' : 'Backend Offline'}
          </Box>
        </Box>

        {/* Main Content */}
        {currentScreen === 'input' ? (
          <ResearchInputScreen onResearchComplete={handleResearchComplete} />
        ) : (
          <ResearchResultsScreen
            results={researchResults}
            onNewResearch={handleNewResearch}
          />
        )}

        {/* Footer */}
        <Box
          sx={{
            textAlign: 'center',
            py: 3,
            px: 2,
            mt: 4,
            borderTop: '1px solid rgba(0,0,0,0.1)',
            backgroundColor: 'rgba(255,255,255,0.8)',
          }}
        >
          <Box sx={{ color: 'text.secondary', fontSize: '0.875rem' }}>
            © {new Date().getFullYear()} Albertsons Companies, Inc. | Powered by LangChain AI
          </Box>
        </Box>

        {/* Snackbar Notifications */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert
            onClose={handleCloseSnackbar}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
}

export default App;
