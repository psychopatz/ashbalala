// frontend/src/context/SnackbarContext.jsx
import React, { createContext, useState, useCallback } from 'react';
import { Snackbar, Alert } from '@mui/material';

const SnackbarContext = createContext();

const SnackbarProvider = ({ children }) => {
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success'); // or 'error', 'warning', 'info'

    const showSnackbar = useCallback((message, severity = 'success') => {
      setSnackbarMessage(message);
      setSnackbarSeverity(severity);
      setSnackbarOpen(true);
    }, []);

  const closeSnackbar = () => {
    setSnackbarOpen(false);
  };

  return (
    <SnackbarContext.Provider value={{ showSnackbar }}>
      {children}
      <Snackbar
          open={snackbarOpen}
          autoHideDuration={5000}
          onClose={closeSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
        <Alert onClose={closeSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </SnackbarContext.Provider>
  );
};

export { SnackbarContext, SnackbarProvider };