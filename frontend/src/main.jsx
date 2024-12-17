// frontend/src/main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { SnackbarProvider } from './context/SnackbarContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <SnackbarProvider>
        <App />
    </SnackbarProvider>
  </StrictMode>,
)