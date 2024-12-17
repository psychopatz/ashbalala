// frontend/src/components/Navbar.jsx
import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Drawer, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import ContactMailIcon from '@mui/icons-material/ContactMail';


const navItems = [
    {
      id: 1,
      label: 'Home',
      path: '/',
      icon: <HomeIcon/>
    },
    {
      id: 2,
      label: 'About',
      path: '/about',
       icon: <InfoIcon/>
    },
     {
        id: 3,
        label: 'Contact',
        path: '/contact',
        icon: <ContactMailIcon/>
      },
  ];

function Navbar() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleNavigation = (path) => {
      navigate(path);
      setDrawerOpen(false);
  }

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2, display: { md: 'none' } }}
            onClick={handleDrawerToggle}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            My App
          </Typography>
          {/* Desktop Navigation */}
            <div sx={{ display: { xs: 'none', md: 'flex' } }}>
                {navItems.map((item) => (
                <Button key={item.id} color="inherit" onClick={() => handleNavigation(item.path)}>
                    {item.label}
                </Button>
                ))}
            </div>
        </Toolbar>
      </AppBar>
      {/* Mobile Navigation Drawer */}
      <Drawer
        open={drawerOpen}
        onClose={handleDrawerToggle}
        sx={{ display: { md: 'none' } }}
      >
          <List>
                {navItems.map((item) => (
                  <ListItem button key={item.id} onClick={() => handleNavigation(item.path)}>
                    <ListItemIcon>
                         {item.icon}
                    </ListItemIcon>
                    <ListItemText primary={item.label} />
                </ListItem>
                ))}
            </List>
        </Drawer>
    </>
  );
}

export default Navbar;