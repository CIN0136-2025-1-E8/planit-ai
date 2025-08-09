import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {signInWithEmailAndPassword} from 'firebase/auth';
import {auth} from './firebase-config';
import {Alert, AppBar, Box, Button, CircularProgress, Container, Paper, TextField, Toolbar, Typography,} from '@mui/material';
import logo from './assets/logo.png';

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    setError('');
    setIsLoading(true);
    try {
      await signInWithEmailAndPassword(auth, email, password);
      navigate('/planit');
    } catch (err: any) {
      setError('Email ou senha inválidos.');
      setIsLoading(false);
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    handleLogin();
  };

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
      <AppBar position="static" sx={{backgroundColor: '#f5f5f5', boxShadow: 'none', color: 'black'}}>
        <Toolbar>
          <Box display="flex" alignItems="center" sx={{flexGrow: 1}}>
            <img src={logo} alt="Planit Logo" style={{height: 40, marginRight: 8}}/>
            <Typography variant="h6" sx={{fontWeight: 'bold', color: '#3b82f6'}}>
              Planit
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>

      <Container component="main" maxWidth="xs" sx={{display: 'flex', alignItems: 'center', flexGrow: 1}}>
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
            borderRadius: '12px',
          }}
        >
          <Typography component="h1" variant="h5" sx={{mb: 3}}>
            Login
          </Typography>
          {error && <Alert severity="error" sx={{width: '100%', mb: 2}}>{error}</Alert>}
          <Box component="form" noValidate sx={{mt: 1, width: '100%'}} onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Endereço de Email"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Senha"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={isLoading}
              sx={{
                mt: 3,
                mb: 2,
                backgroundColor: '#3b82f6',
                fontWeight: 'bold',
                textTransform: 'none',
                borderRadius: '12px',
                py: 1.5,
                height: 52.5
              }}
            >
              {isLoading ? <CircularProgress size={24} sx={{ color: 'white' }}/> : 'Entrar'}
            </Button>
            <Box sx={{textAlign: 'center'}}>
              <Link to="/register" style={{color: '#3b82f6', textDecoration: 'none'}}>
                <Typography>Não tem uma conta? Registre-se</Typography>
              </Link>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}
