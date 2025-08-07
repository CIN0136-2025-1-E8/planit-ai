import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {createUserWithEmailAndPassword} from 'firebase/auth';
import {auth} from './firebase-config';
import {Alert, AppBar, Box, Button, Container, Paper, TextField, Toolbar, Typography,} from '@mui/material';
import logo from './assets/logo.png';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export default function RegistrationPage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [nickname, setNickname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async () => {
    if (!name || !email || !password) {
      setError('Por favor, preencha os campos obrigatórios.');
      return;
    }

    const registerWithBackend = async (token: string) => {
      const formData = new FormData();
      formData.append('name', name);
      if (nickname) {
        formData.append('nickname', nickname);
      }

      const response = await fetch(`${API_BASE_URL}/api/user/register`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        let errorData = {detail: 'Erro desconhecido do servidor.'};
        try {
          errorData = JSON.parse(errorText);
        } catch (e) {
          console.error("Could not parse error response as JSON:", errorText);
        }
        throw {status: response.status, data: errorData};
      }
    };

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      const token = await user.getIdToken(true);

      try {
        await registerWithBackend(token);
        navigate('/planit');
      } catch (initialError: any) {
        if (initialError.status === 401) {
          await new Promise(resolve => setTimeout(resolve, 2000));
          const freshToken = await user.getIdToken(true);
          await registerWithBackend(freshToken);
          navigate('/planit');
        } else {
          throw new Error(initialError.data?.detail || 'Falha ao registrar no backend.');
        }
      }
    } catch (err: any) {
      if (err.code === 'auth/email-already-in-use') {
        setError('Este email já está em uso. Por favor, tente fazer login.');
      } else {
        setError(err.message || 'Ocorreu um erro durante o registro.');
      }
    }
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
            Criar Conta
          </Typography>
          {error && <Alert severity="error" sx={{width: '100%', mb: 2}}>{error}</Alert>}
          <Box component="form" noValidate sx={{mt: 1, width: '100%'}}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="name"
              label="Nome Completo"
              name="name"
              autoComplete="name"
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <TextField
              margin="normal"
              fullWidth
              id="nickname"
              label="Apelido (opcional)"
              name="nickname"
              autoComplete="nickname"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Endereço de Email"
              name="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Senha"
              type="password"
              id="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="button"
              fullWidth
              variant="contained"
              onClick={handleRegister}
              sx={{
                mt: 3,
                mb: 2,
                backgroundColor: '#3b82f6',
                fontWeight: 'bold',
                textTransform: 'none',
                borderRadius: '12px',
                py: 1.5,
              }}
            >
              Registrar
            </Button>
            <Box sx={{textAlign: 'center'}}>
              <Link to="/login" style={{color: '#3b82f6', textDecoration: 'none'}}>
                <Typography>Já tem uma conta? Faça login</Typography>
              </Link>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}
