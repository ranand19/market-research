import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  CircularProgress,
  LinearProgress,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Remove as MinimizeIcon,
  OpenInFull as ExpandIcon,
  RadioButtonUnchecked as PendingIcon,
} from '@mui/icons-material';

const STEPS = [
  { key: 'research', label: 'Research', description: 'Gathering data via web search' },
  { key: 'analyze', label: 'Analysis', description: 'Analyzing gathered data' },
  { key: 'strategize', label: 'Strategy', description: 'Generating recommendations' },
  { key: 'compile', label: 'Compile', description: 'Building final report' },
];

const statusIcon = (status) => {
  switch (status) {
    case 'running':
      return <CircularProgress size={20} sx={{ color: '#0066cc' }} />;
    case 'completed':
      return <CheckCircleIcon sx={{ color: '#4caf50', fontSize: 22 }} />;
    case 'error':
      return <ErrorIcon sx={{ color: '#d32f2f', fontSize: 22 }} />;
    default:
      return <PendingIcon sx={{ color: '#bdbdbd', fontSize: 22 }} />;
  }
};

const statusColor = (status) => {
  switch (status) {
    case 'running':
      return '#e3f2fd';
    case 'completed':
      return '#e8f5e9';
    case 'error':
      return '#ffebee';
    default:
      return 'transparent';
  }
};

const TracePanel = ({ steps, isActive }) => {
  const [minimized, setMinimized] = useState(false);

  if (!isActive) return null;

  return (
    <Paper
      elevation={6}
      sx={{
        position: 'fixed',
        bottom: 24,
        right: 24,
        width: 320,
        zIndex: 1300,
        borderRadius: 2,
        overflow: 'hidden',
        border: '1px solid rgba(0, 61, 165, 0.2)',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          px: 2,
          py: 1,
          background: 'linear-gradient(135deg, #003da5 0%, #0066cc 100%)',
          color: 'white',
        }}
      >
        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
          Agent Workflow
        </Typography>
        <IconButton
          size="small"
          onClick={() => setMinimized(!minimized)}
          sx={{ color: 'white' }}
        >
          {minimized ? <ExpandIcon fontSize="small" /> : <MinimizeIcon fontSize="small" />}
        </IconButton>
      </Box>

      {/* Steps */}
      {!minimized && (
        <Box sx={{ p: 1.5 }}>
          {STEPS.map((step, idx) => {
            const stepData = steps[step.key] || {};
            const status = stepData.status || 'pending';
            const iteration = stepData.iteration || 0;
            const maxIterations = stepData.maxIterations || 0;
            const progress = maxIterations > 0
              ? Math.min(100, Math.round((iteration / maxIterations) * 100))
              : 0;
            return (
              <Box
                key={step.key}
                sx={{
                  px: 1.5,
                  py: 1,
                  borderRadius: 1,
                  backgroundColor: statusColor(status),
                  mb: idx < STEPS.length - 1 ? 0.5 : 0,
                  transition: 'background-color 0.3s ease',
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                  {statusIcon(status)}
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 600, lineHeight: 1.3 }}>
                      {step.label}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {status === 'running'
                        ? (iteration > 0
                          ? `${step.description} (${iteration}/${maxIterations})`
                          : step.description)
                        : status === 'completed'
                        ? 'Done'
                        : status === 'error'
                        ? 'Failed'
                        : 'Waiting'}
                    </Typography>
                  </Box>
                </Box>
                {status === 'running' && maxIterations > 0 && (
                  <LinearProgress
                    variant="determinate"
                    value={progress}
                    sx={{
                      mt: 0.75,
                      ml: 4.5,
                      height: 4,
                      borderRadius: 2,
                      backgroundColor: 'rgba(0, 102, 204, 0.12)',
                      '& .MuiLinearProgress-bar': {
                        borderRadius: 2,
                        backgroundColor: '#0066cc',
                      },
                    }}
                  />
                )}
              </Box>
            );
          })}
        </Box>
      )}
    </Paper>
  );
};

export default TracePanel;
