// frontend/src/theme/theme.js
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        mode: 'light', // Set the default mode to light
        primary: {
            main: '#2196f3', // Slightly brighter primary
            light: '#6ec6ff',
            dark: '#0069c0',
            contrastText: '#fff',
        },
        secondary: {
            main: '#e91e63',
            light: '#ff6090',
            dark: '#b00036',
            contrastText: '#fff',
        },
        background: {
            default: '#f5f5f5', // Light grey background
            paper: '#fff', // White paper background
        },
        text: {
            primary: 'rgba(0, 0, 0, 0.87)', // Dark grey text
            secondary: 'rgba(0, 0, 0, 0.6)',
        },
    },
    darkMode: {
        palette: {
            mode: 'dark',
            primary: {
                main: '#64b5f6', // Example dark mode primary
                light: '#9be7ff',
                dark: '#2286c3',
                contrastText: '#000',
            },
            secondary: {
                main: '#f06292', // Example dark mode secondary
                light: '#ff94c2',
                dark: '#ba2d65',
                contrastText: '#000',
            },
            background: {
                default: '#303030', // Dark grey background
                paper: '#424242', // Dark paper background
            },
            text: {
                primary: '#fff',  // White text
                secondary: '#ddd', // Light grey text
            },
        },
    },
    components: {
        MuiTypography: {
            styleOverrides: {
                root: ({ theme }) => ({
                color: theme.palette.text.primary,
                }),
            },
        },
        MuiButton: {
           styleOverrides: {
                root: ({ theme }) => ({
                    color: theme.palette.text.primary,
                })
           }
        }
    },
});

export default theme;