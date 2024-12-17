// frontend/src/App.jsx
import React from 'react';
import AppRoutes from './routes/routes';
import { BrowserRouter } from 'react-router-dom';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
        <Navbar/>
        <AppRoutes />
     </BrowserRouter>
  );
}

export default App;