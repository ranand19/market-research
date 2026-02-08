import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Grid,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Close as CloseIcon,
  TrendingUp as TrendingUpIcon,
  Business as BusinessIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
} from '@mui/icons-material';
import apiService from '../services/apiService';

const ResearchInputScreen = ({ onResearchComplete }) => {
  const [query, setQuery] = useState('');
  const [researchType, setResearchType] = useState('market_overview');
  const [companyName, setCompanyName] = useState('');
  const [industry, setIndustry] = useState('');
  const [competitors, setCompetitors] = useState([]);
  const [competitorInput, setCompetitorInput] = useState('');
  const [researchTypes, setResearchTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadResearchTypes();
  }, []);

  const loadResearchTypes = async () => {
    try {
      const types = await apiService.getResearchTypes();
      setResearchTypes(types);
    } catch (err) {
      console.error('Failed to load research types:', err);
    }
  };

  const handleAddCompetitor = () => {
    if (competitorInput.trim() && !competitors.includes(competitorInput.trim())) {
      setCompetitors([...competitors, competitorInput.trim()]);
      setCompetitorInput('');
    }
  };

  const handleRemoveCompetitor = (competitor) => {
    setCompetitors(competitors.filter((c) => c !== competitor));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a research query');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const researchData = {
        query: query.trim(),
        research_type: researchType,
        company_name: companyName.trim() || null,
        industry: industry.trim() || null,
        competitors: competitors.length > 0 ? competitors : null,
      };

      const result = await apiService.executeResearch(researchData);
      onResearchComplete(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to execute research. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getResearchIcon = (type) => {
    switch (type) {
      case 'market_overview':
        return <AssessmentIcon />;
      case 'competitor_analysis':
        return <BusinessIcon />;
      case 'trend_analysis':
        return <TrendingUpIcon />;
      case 'full_report':
        return <DescriptionIcon />;
      default:
        return <SearchIcon />;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box
        sx={{
          textAlign: 'center',
          mb: 4,
          background: 'linear-gradient(135deg, #003da5 0%, #0066cc 100%)',
          borderRadius: 3,
          p: 4,
          color: 'white',
        }}
      >
        <Typography variant="h3" gutterBottom sx={{ color: 'white', fontWeight: 700 }}>
          Market Research & Competitor Tracking
        </Typography>
        <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
          AI-Powered Intelligence Platform for Albertsons
        </Typography>
      </Box>

      <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Research Query */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Research Query"
                placeholder="E.g., Analyze the organic food market trends in the Pacific Northwest"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                multiline
                rows={3}
                variant="outlined"
                required
              />
            </Grid>

            {/* Research Type */}
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Research Type</InputLabel>
                <Select
                  value={researchType}
                  label="Research Type"
                  onChange={(e) => setResearchType(e.target.value)}
                >
                  {researchTypes.map((type) => (
                    <MenuItem key={type.id} value={type.id}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getResearchIcon(type.id)}
                        <Box>
                          <Typography variant="body1">{type.name}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {type.description}
                          </Typography>
                        </Box>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* Industry */}
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Industry (Optional)"
                placeholder="E.g., Retail, Grocery, Food & Beverage"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                variant="outlined"
              />
            </Grid>

            {/* Company Name */}
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Company Name (Optional)"
                placeholder="E.g., Albertsons Companies"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                variant="outlined"
              />
            </Grid>

            {/* Competitors Input */}
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  label="Add Competitors (Optional)"
                  placeholder="E.g., Kroger, Walmart"
                  value={competitorInput}
                  onChange={(e) => setCompetitorInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      handleAddCompetitor();
                    }
                  }}
                  variant="outlined"
                />
                <Tooltip title="Add competitor">
                  <IconButton
                    color="primary"
                    onClick={handleAddCompetitor}
                    disabled={!competitorInput.trim()}
                  >
                    <AddIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Grid>

            {/* Competitors Chips */}
            {competitors.length > 0 && (
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {competitors.map((competitor) => (
                    <Chip
                      key={competitor}
                      label={competitor}
                      onDelete={() => handleRemoveCompetitor(competitor)}
                      deleteIcon={<CloseIcon />}
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Grid>
            )}

            {/* Error Alert */}
            {error && (
              <Grid item xs={12}>
                <Alert severity="error" onClose={() => setError(null)}>
                  {error}
                </Alert>
              </Grid>
            )}

            {/* Submit Button */}
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                fullWidth
                disabled={loading || !query.trim()}
                startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                sx={{ py: 1.5, fontSize: '1.1rem' }}
              >
                {loading ? 'Analyzing...' : 'Start Research'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      {/* Quick Tips */}
      <Box sx={{ mt: 3 }}>
        <Paper elevation={1} sx={{ p: 3, backgroundColor: '#f8f9fa' }}>
          <Typography variant="h6" gutterBottom color="primary">
            💡 Research Tips
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                <strong>Market Overview:</strong> Get comprehensive market analysis including size, trends, and opportunities
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                <strong>Competitor Analysis:</strong> Deep dive into competitor strategies, strengths, and weaknesses
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                <strong>Trend Analysis:</strong> Identify emerging trends and predict future market directions
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Container>
  );
};

export default ResearchInputScreen;
