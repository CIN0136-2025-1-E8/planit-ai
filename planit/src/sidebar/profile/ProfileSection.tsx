import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut, deleteUser as deleteFirebaseUser } from 'firebase/auth';
import { auth } from '../../firebase-config.ts';
import { useAuth } from '../../AuthContext.tsx';
import {
  Box,
  Button,
  Typography,
  Divider,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Logout, DeleteForever, ClearAll } from '@mui/icons-material';
import { clearChatHistory, deleteUserAccount } from './api.ts';

export default function ProfileSection() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [openClearDialog, setOpenClearDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await signOut(auth);
      navigate('/login');
    } catch (err) {
      setError('Falha ao fazer logout. Tente novamente.');
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    setOpenClearDialog(false);
    setIsLoading(true);
    setError('');
    setSuccess('');
    try {
      const token = await currentUser?.getIdToken();
      if (!token) throw new Error('Não foi possível obter o token de autenticação.');

      const response = await clearChatHistory(token);

      if (!response.ok) {
        throw new Error('Falha ao limpar o histórico de chat.');
      }
      setSuccess('Histórico de chat limpo com sucesso!');
    } catch (err: any) {
      setError(err.message || 'Ocorreu um erro.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    setOpenDeleteDialog(false);
    setIsLoading(true);
    setError('');
    try {
      const token = await currentUser?.getIdToken(true);
      if (!token) throw new Error('Não foi possível obter o token de autenticação.');

      const response = await deleteUserAccount(token);
      if (!response.ok) {
        throw new Error('Falha ao apagar os dados da conta no servidor.');
      }

      if (currentUser) {
        await deleteFirebaseUser(currentUser);
      }

      navigate('/login');

    } catch (err: any) {
      setError(err.message || 'Ocorreu um erro ao apagar a conta. Por favor, tente fazer login novamente e repetir o processo.');
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Perfil e Configurações
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        {currentUser?.email}
      </Typography>
      <Divider sx={{ mb: 2 }} />

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Button
          variant="outlined"
          startIcon={<Logout />}
          onClick={handleLogout}
          disabled={isLoading}
        >
          Sair
        </Button>
        <Button
          variant="outlined"
          color="warning"
          startIcon={<ClearAll />}
          onClick={() => setOpenClearDialog(true)}
          disabled={isLoading}
        >
          Limpar Conversa
        </Button>
        <Button
          variant="contained"
          color="error"
          startIcon={<DeleteForever />}
          onClick={() => setOpenDeleteDialog(true)}
          disabled={isLoading}
        >
          Apagar Conta
        </Button>
      </Box>

      {isLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
          <CircularProgress />
        </Box>
      )}

      <Dialog open={openClearDialog} onClose={() => setOpenClearDialog(false)}>
        <DialogTitle>Limpar Histórico?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Esta ação é irreversível. Todo o seu histórico de conversas será permanentemente apagado.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenClearDialog(false)}>Cancelar</Button>
          <Button onClick={handleClearHistory} color="warning">
            Limpar
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle>Apagar conta permanentemente?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Esta ação é irreversível. Todos os seus dados, incluindo perfil, matérias e histórico, serão apagados.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>Cancelar</Button>
          <Button onClick={handleDeleteAccount} color="error">
            Apagar Minha Conta
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}