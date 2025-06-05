import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';

export default function HomePage() {
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Barra superior */}
      <AppBar position="static" sx={{ backgroundColor: '#f5f5f5', boxShadow: 'none', color: 'black' }}>
        <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <Box display="flex" alignItems="center">
            <img src="/logo.png" alt="Planit Logo" style={{ height: 40, marginRight: 8 }} />
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
            >
              Experimente o Planit
            </Button>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Conteúdo centralizado no restante da tela */}
      <Box
        sx={{
          flex: 1,
          backgroundColor: '#040032',
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'left',
          px: 4,
        }}
      >
        <Box>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#fff' }}>
            Organize sua
          </Typography>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#fff' }}>
            vida de
          </Typography>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#fff' }}>
            estudos com{' '}
            <Box component="span" sx={{ color: '#60a5fa' }}>
              Planit
            </Box>
            .
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}
