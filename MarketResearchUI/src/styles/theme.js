import { createTheme } from '@mui/material/styles';

// Albertsons brand colors
const albertsonsBlue = '#003da5';
const albertsonsLightBlue = '#0066cc';
const albertsonsOrange = '#ff6b35';
const albertsonsGray = '#6c757d';
const albertsonsLightGray = '#f8f9fa';

const theme = createTheme({
  palette: {
    primary: {
      main: albertsonsBlue,
      light: albertsonsLightBlue,
      dark: '#002a73',
      contrastText: '#ffffff',
    },
    secondary: {
      main: albertsonsOrange,
      light: '#ff8c5a',
      dark: '#e64a1f',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f5f7fa',
      paper: '#ffffff',
    },
    text: {
      primary: '#212529',
      secondary: albertsonsGray,
    },
    success: {
      main: '#28a745',
    },
    info: {
      main: albertsonsLightBlue,
    },
    warning: {
      main: '#ffc107',
    },
    error: {
      main: '#dc3545',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      color: albertsonsBlue,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      color: albertsonsBlue,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      color: albertsonsBlue,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '8px',
          padding: '10px 24px',
          fontSize: '1rem',
          fontWeight: 600,
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0, 61, 165, 0.2)',
          '&:hover': {
            boxShadow: '0 4px 8px rgba(0, 61, 165, 0.3)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.12)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: '8px',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '6px',
          fontWeight: 500,
        },
      },
    },
  },
});

export default theme;
