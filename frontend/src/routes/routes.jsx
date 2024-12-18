import React from 'react';
import { Route, Routes } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import AboutPage from '../pages/AboutPage';
import ContactPage from '../pages/ContactPage';
import AudioPlayerPage from '../pages/AudioPlayerPage';

function AppRoutes() {
return (
    <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/audio" element={<AudioPlayerPage />} />
    </Routes>
);
}

export default AppRoutes;
