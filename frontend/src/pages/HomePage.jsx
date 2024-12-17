 // frontend/src/pages/HomePage.jsx
 import React from 'react';
 import useSnackbar from '../hooks/useSnackbar';
 import { Box } from '@mui/material';

 function HomePage() {
     const { showSnackbar } = useSnackbar();

     const handleSuccess = () => {
         showSnackbar('This is a success message!', 'success');
     };
     const handleError = () => {
         showSnackbar('This is an error message!', 'error')
     }
     const handleWarning = () => {
         showSnackbar('This is a warning message!', 'warning')
     }
     const handleInfo = () => {
         showSnackbar('This is an info message!', 'info')
     }

     return (
          <Box sx={{ backgroundColor: 'background.default', minHeight: '100vh', padding: 2 }}>
              <h1>Welcome to the Home Page</h1>
              <p>This is a simple homepage.</p>
              <button onClick={handleSuccess}>Show Success Snackbar</button>
              <button onClick={handleError}>Show Error Snackbar</button>
              <button onClick={handleWarning}>Show Warning Snackbar</button>
              <button onClick={handleInfo}>Show Info Snackbar</button>
         </Box>
     );
 }

 export default HomePage;