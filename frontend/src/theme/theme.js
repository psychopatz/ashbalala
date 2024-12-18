// frontend/src/theme/theme.js
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
 palette: {
     mode: 'light',
     primary: {
         main: '#2196f3',
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
         default: '#f5f5f5',
         paper: '#fff',
     },
     text: {
         primary: 'rgba(0, 0, 0, 0.87)',
         secondary: 'rgba(0, 0, 0, 0.6)',
     },
 },
 darkMode: {
     palette: {
         mode: 'dark',
         primary: {
             main: '#64b5f6',
             light: '#9be7ff',
             dark: '#2286c3',
             contrastText: '#000',
         },
         secondary: {
             main: '#f06292',
             light: '#ff94c2',
             dark: '#ba2d65',
             contrastText: '#000',
         },
         background: {
             default: '#303030',
             paper: '#424242',
         },
         text: {
             primary: '#fff',
             secondary: '#ddd',
         },
     },
 },
 components: {
     MuiCssBaseline: {
         styleOverrides: {
             body: {
                 margin: 0,
             },
             '#root': {
                 margin: 0,
             }
         },
     },
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
    },
    MuiCard: {
        styleOverrides: {
             root: ({ theme }) => ({
                backgroundColor: theme.palette.background.paper,
            }),
         }
     },
     MuiLinearProgress: {
         styleOverrides: {
           root: ({ theme }) => ({
             backgroundColor: theme.palette.grey[300],
           }),
           bar: ({ theme }) => ({
              backgroundColor: theme.palette.primary.main,
          }),
         },
      },
   },
});

export default theme;