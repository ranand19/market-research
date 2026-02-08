import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Divider,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Download as DownloadIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Business as BusinessIcon,
  Lightbulb as LightbulbIcon,
} from '@mui/icons-material';

const ResearchResultsScreen = ({ results, onNewResearch }) => {
  const [expandedSection, setExpandedSection] = useState(false);

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpandedSection(isExpanded ? panel : false);
  };

  const handleDownload = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `research_${results.research_id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const renderListItems = (items) => {
    if (Array.isArray(items)) {
      return (
        <List>
          {items.map((item, index) => (
            <ListItem key={index}>
              <ListItemIcon>
                <CheckCircleIcon color="success" />
              </ListItemIcon>
              <ListItemText primary={item} />
            </ListItem>
          ))}
        </List>
      );
    }
    return null;
  };

  const renderResultSection = (title, data, icon, color = 'primary') => {
    if (!data) return null;

    return (
      <Accordion
        expanded={expandedSection === title}
        onChange={handleAccordionChange(title)}
        sx={{ mb: 2 }}
      >
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{
            backgroundColor: `${color}.50`,
            '&:hover': {
              backgroundColor: `${color}.100`,
            },
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {icon}
            <Typography variant="h6">{title}</Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          {typeof data === 'object' && !Array.isArray(data) ? (
            Object.entries(data).map(([key, value]) => (
              <Box key={key} sx={{ mb: 2 }}>
                <Typography variant="subtitle1" color="primary" sx={{ fontWeight: 600, mb: 1 }}>
                  {key.replace(/_/g, ' ').toUpperCase()}
                </Typography>
                {Array.isArray(value) ? (
                  renderListItems(value)
                ) : typeof value === 'object' ? (
                  <pre style={{ backgroundColor: '#f5f5f5', padding: '12px', borderRadius: '8px', overflow: 'auto' }}>
                    {JSON.stringify(value, null, 2)}
                  </pre>
                ) : (
                  <Typography variant="body1" color="text.secondary" sx={{ pl: 2 }}>
                    {value}
                  </Typography>
                )}
              </Box>
            ))
          ) : (
            <Typography variant="body1">{JSON.stringify(data, null, 2)}</Typography>
          )}
        </AccordionDetails>
      </Accordion>
    );
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={onNewResearch}
            variant="outlined"
            color="primary"
          >
            New Research
          </Button>
          <Button
            startIcon={<DownloadIcon />}
            onClick={handleDownload}
            variant="contained"
            color="secondary"
          >
            Download Report
          </Button>
        </Box>

        <Paper
          elevation={3}
          sx={{
            p: 3,
            background: 'linear-gradient(135deg, #003da5 0%, #0066cc 100%)',
            color: 'white',
          }}
        >
          <Typography variant="h4" gutterBottom sx={{ color: 'white', fontWeight: 700 }}>
            Research Results
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
            <Chip
              label={`ID: ${results.research_id}`}
              sx={{ backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
            <Chip
              label={results.research_type.replace(/_/g, ' ').toUpperCase()}
              sx={{ backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
            <Chip
              label={`Status: ${results.status}`}
              sx={{ backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
            <Chip
              label={new Date(results.timestamp).toLocaleString()}
              sx={{ backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
          </Box>
        </Paper>
      </Box>

      {/* Executive Summary */}
      <Paper elevation={2} sx={{ p: 3, mb: 3, backgroundColor: '#f8f9fa' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <LightbulbIcon color="warning" sx={{ fontSize: 32 }} />
          <Typography variant="h5" color="primary">
            Executive Summary
          </Typography>
        </Box>
        <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
          {results.summary}
        </Typography>
      </Paper>

      {/* Results by Type */}
      <Box>
        {results.research_type === 'full_report' ? (
          <>
            {results.results.market_analysis &&
              renderResultSection(
                'Market Analysis',
                results.results.market_analysis,
                <AssessmentIcon color="primary" />,
                'primary'
              )}
            {results.results.competitor_analysis &&
              renderResultSection(
                'Competitor Analysis',
                results.results.competitor_analysis,
                <BusinessIcon color="secondary" />,
                'secondary'
              )}
            {results.results.trend_analysis &&
              renderResultSection(
                'Trend Analysis',
                results.results.trend_analysis,
                <TrendingUpIcon color="success" />,
                'success'
              )}
            {results.results.executive_summary && (
              <Alert severity="info" sx={{ mt: 2 }}>
                <Typography variant="body2">
                  {results.results.executive_summary}
                </Typography>
              </Alert>
            )}
          </>
        ) : (
          renderResultSection(
            results.research_type.replace(/_/g, ' ').toUpperCase(),
            results.results,
            <AssessmentIcon color="primary" />,
            'primary'
          )
        )}
      </Box>

      {/* Detailed Results Card */}
      <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom color="primary">
          📊 Detailed Analysis Data
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Box
          sx={{
            maxHeight: '400px',
            overflow: 'auto',
            backgroundColor: '#f5f5f5',
            p: 2,
            borderRadius: 2,
          }}
        >
          <pre style={{ margin: 0, fontSize: '0.875rem' }}>
            {JSON.stringify(results.results, null, 2)}
          </pre>
        </Box>
      </Paper>

      {/* Action Items */}
      <Paper elevation={2} sx={{ p: 3, mt: 3, backgroundColor: '#e3f2fd' }}>
        <Typography variant="h6" gutterBottom color="primary">
          🎯 Next Steps
        </Typography>
        <List>
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Review detailed findings"
              secondary="Analyze each section for actionable insights"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Share with stakeholders"
              secondary="Download and distribute the report to relevant teams"
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircleIcon color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Develop action plan"
              secondary="Create strategic initiatives based on research findings"
            />
          </ListItem>
        </List>
      </Paper>
    </Container>
  );
};

export default ResearchResultsScreen;
