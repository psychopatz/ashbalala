// frontend/src/context/ThemeContext.jsx
import React, { createContext, useState, useMemo } from 'react';
 import { createTheme, ThemeProvider } from '@mui/material/styles';
 import baseTheme from '../theme/theme'; // Import your base theme

 const ThemeContext = createContext();

 const ThemeProviderWrapper = ({ children }) => {
 const [darkMode, setDarkMode] = useState(false);

 const theme = useMemo(
     () =>
     createTheme(
         darkMode ? { ...baseTheme, ...baseTheme.darkMode } : baseTheme,
     ),
     [darkMode],
 );

 const toggleTheme = () => {
     setDarkMode((prevMode) => !prevMode);
 };


 return (
     <ThemeContext.Provider value={{ darkMode, toggleTheme }}>
         <ThemeProvider theme={theme}>
             {children}
         </ThemeProvider>
     </ThemeContext.Provider>
 );
 };

 export { ThemeContext, ThemeProviderWrapper };