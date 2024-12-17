import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { SnackbarProvider } from './context/SnackbarContext.jsx'
import { ThemeProviderWrapper } from './context/ThemeContext.jsx';
import { CssBaseline } from '@mui/material';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <CssBaseline>
            <ThemeProviderWrapper>
                <SnackbarProvider>
                    <App />
                </SnackbarProvider>
            </ThemeProviderWrapper>
        </CssBaseline>
    </StrictMode>,
)
