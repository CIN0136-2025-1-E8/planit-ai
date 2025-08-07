// import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import Grid from '@mui/material/Grid';
import logo from './assets/logo.png'; 
import { useNavigate } from 'react-router-dom';

export default function HomePage() {
  const navigate = useNavigate();
  return (
    <Box
      sx={{
        minHeight: '100vh',
        width: '100vw',
        display: 'flex',
        flexDirection: 'column',
        position: 'absolute',
        top: 0,
        left: 0,
        bgcolor: '#040032', 
        color: '#fff',
      }}
    >
      {/* Barra superior */}
      <AppBar position="static" sx={{ backgroundColor: '#f5f5f5', boxShadow: 'none', color: 'black' }}>
        <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Box display="flex" alignItems="center">
            <img src={logo} alt="Planit Logo" style={{ height: 40, marginRight: 8 }} />
            <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#3b82f6' }}>
              Planit
            </Typography>
          </Box>
          <Box>
            <Button variant="text" sx={{ fontWeight: 'bold', color: '#3b82f6', textTransform: 'none' }}>
              Login
            </Button>
            <Button
              variant="contained"
              sx={{
                ml: 2,
                backgroundColor: '#3b82f6',
                fontWeight: 'bold',
                textTransform: 'none',
                borderRadius: '12px'
              }}
              onClick={()=> navigate("/planit")}
            >
              Experimente o Planit
            </Button>
          </Box>
        </Toolbar>
      </AppBar>

      
      <Box
        sx={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          px: 0,
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
           {/* Removed the Grid item here */}
    <Box>
      <Typography variant="h2" sx={{ fontWeight: 'bold', color: '#fff', mb: 2 }}>
        Organize sua vida de estudos com{' '}
        <Box component="span" sx={{ color: '#60a5fa' }}>
          Planit
        </Box>
        .
      </Typography>
      <Typography variant="h5" sx={{ color: '#cbd5e1', mb: 4 }}>
        Uma plataforma inteligente para planejar, acompanhar e otimizar seus estudos.
      </Typography>
      <Button
        variant="contained"
        size="large"
        sx={{
          backgroundColor: '#3b82f6',
          fontWeight: 'bold',
          textTransform: 'none',
          borderRadius: '12px',
          px: 4,
          py: 1.5,
          fontSize: '1.2rem'
        }}
        onClick={() => navigate("/planit")}
      >
        Experimente o Planit
      </Button>
    </Box>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
}
