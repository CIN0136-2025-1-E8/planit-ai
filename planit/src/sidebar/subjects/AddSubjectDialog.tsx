import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  IconButton,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

type AddSubjectDialogProps = {
  open: boolean;
  onClose: () => void;
  onSubmit: (name: string, file: File | null) => void;
  loading?: boolean;
};

export default function AddSubjectDialog({
  open,
  onClose,
  onSubmit,
  loading = false,
}: AddSubjectDialogProps) {
  const [name, setName] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !file) return;
    onSubmit(name.trim(), file);
    setName("");
    setFile(null);
  };

  const handleClose = () => {
    setName("");
    setFile(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="xs" fullWidth>
      <DialogTitle>
        Adicione Mais uma matéria ao seu calendário!
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={{ position: "absolute", right: 8, top: 8 }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          <Typography sx={{ mb: 2 }}>
            Adicione abaixo o arquivo do plano da matéria (PDF) e uma descrição.
          </Typography>
          <TextField
            label="Nome/Descrição da Matéria"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            required
            sx={{ mb: 2 }}
          />
          <Button
            variant="outlined"
            component="label"
            fullWidth
            sx={{ mb: 1 }}
          >
            {file ? file.name : "Escolher arquivo PDF"}
            <input
              type="file"
              accept="application/pdf"
              hidden
              onChange={handleFileChange}
            />
          </Button>
          {file && (
            <Typography variant="body2" color="textSecondary">
              {file.name}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="secondary">
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading || !name.trim() || !file}
          >
            Adicionar
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}