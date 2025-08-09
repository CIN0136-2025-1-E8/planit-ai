import {useEffect, useState} from "react";
import {Box, Button, IconButton, Paper, Typography,} from "@mui/material";
import {Add, Delete, ExpandLess, ExpandMore} from "@mui/icons-material";
import AddSubjectDialog from "./AddSubjectDialog";
import {addSubject, deleteSubject, fetchSubjects, type Subject} from './api';

// Expanded color palette for new subjects
const subjectColorPalette = [
  "#9c27b0", // purple
  "#4caf50", // green
  "#ff9800", // orange
  "#e91e63", // pink
  "#1976d2", // blue (primary)
  "#3b82f6", // light blue (from your homepage)
  "#ffb74d", // light orange
  "#64b5f6", // light blue
  "#81c784", // light green
  "#f06292", // pink accent
  "#ba68c8", // purple accent
  "#ffd54f", // yellow accent
  "#a1887f", // brown/neutral
  "#90caf9", // very light blue
  "#f44336", // red
  "#00bcd4", // cyan
  "#388e3c", // dark green
  "#fbc02d", // yellow
  "#8d6e63", // brown
  "#bdbdbd", // grey
]

// Helper to pick a random color
function getRandomSubjectColor() {
  return subjectColorPalette[Math.floor(Math.random() * subjectColorPalette.length)];
}

export default function SubjectsSection({ onCalendarUpdate }: { onCalendarUpdate: () => void }) {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchSubjects()
      .then(fetched => setSubjects(
        fetched.map(subj => ({
          ...subj,
          color: getRandomSubjectColor(),
          expanded: false,

        }))
      ))
      .catch((err) => {
        console.error(err);
        setError("Não foi possível carregar as matérias. Por favor, tente fazer o login novamente.");
        setSubjects([]);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleToggle = (id: string) => {
    setSubjects((prev) =>
      prev.map((s) =>
        s.id === id ? { ...s, expanded: !s.expanded } : s
      )
    );
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteSubject(id);
      setSubjects((prev) => prev.filter((s) => s.id !== id));
      onCalendarUpdate();
    } catch (err: any) {
      setError(err.message || "Erro ao remover matéria.");
    }
  };

  // New handler for dialog submit
  const handleDialogSubmit = async (title: string, file: File | null) => {
    if (!title || !file) return;
    setAdding(true);
    setError(null);
    try {
      const created = await addSubject(title, file);
      // Normalize the created subject to ensure id and title are present
      const normalized = {
        ...created,
        id: created.id || created.uuid || '',
        title: created.title || created.name || title,
        color: getRandomSubjectColor(),
        expanded: true,
      };
      setSubjects((prev) => [...prev, normalized]);
      onCalendarUpdate();
      setDialogOpen(false);
    } catch (err: any) {
      setError(err.message || "Erro ao adicionar matéria.");
    } finally {
      setAdding(false);
    }
  };

  return (
    <Box sx={{ p: 2, height: "100%", overflowY: "auto" }} className="custom-scrollbar">
      <Typography variant="h6" sx={{ mb: 2 }}>
        Matérias
      </Typography>
      {error && <Typography color="error">{error}</Typography>}
      {loading ? (
        <Typography>Carregando...</Typography>
      ) : (
        subjects.map((subject) => (
          <Paper

            key={subject.id} // use id as key


            sx={{
              mb: 2,
              p: 1.5,
              bgcolor: subject.color || "#bdbdbd",
              borderRadius: 3,
              boxShadow: "none",
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <IconButton
                  size="small"

                  onClick={() => handleToggle(subject.id)}

                  sx={{ color: "#fff" }}
                >
                  {subject.expanded ? <ExpandLess /> : <ExpandMore />}
                </IconButton>
                <Typography variant="subtitle1" sx={{ color: "#fff", fontWeight: 600 }}>
                  {subject.title}
                </Typography>
              </Box>
              <IconButton
                size="small"

                onClick={() => handleDelete(subject.id)}

                sx={{ color: "#fff" }}
                aria-label="Remover matéria"
              >
                <Delete />
              </IconButton>
            </Box>
            {/* Remove the Arquivos section */}
          </Paper>
        ))
      )}
      {/* Add new subject */}
      <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
        <Button
          variant="contained"
          color="success"
          onClick={() => setDialogOpen(true)}
          startIcon={<Add />}
          sx={{ borderRadius: 2, minWidth: 0, px: 2, flex: 1 }}
        >
          Nova Matéria
        </Button>
      </Box>
      <AddSubjectDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSubmit={handleDialogSubmit}
        loading={adding}
      />
    </Box>
  );
}