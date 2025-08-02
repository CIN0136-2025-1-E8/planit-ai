// import React, { useEffect, useState } from "react";
import { useEffect, useState } from "react";
import {
  Box,
  Paper,
  Typography,
  Button,
  IconButton,

} from "@mui/material";
// import { ExpandLess, ExpandMore, Delete, Add, Description } from "@mui/icons-material";
import { ExpandLess, ExpandMore, Delete, Add } from "@mui/icons-material";
import AddSubjectDialog from "./AddSubjectDialog";

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// Subject and file types
type Subject = {
  id: string;
  title: string; // changed from name to title
  color: string;
  files: { name: string; url: string }[];
  expanded?: boolean;
};

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

// Helper: get color for subject (fallbacks for demo)
const subjectColors: Record<string, string> = {
  Desenvolvimento: "#e57373",
  "Mat Discreta": "#64b5f6",
  "Sistemas Digitais": "#81c784",
  IP: "#bdbdbd",
  CAD: "#ffb74d",
};

async function fetchSubjects(): Promise<Subject[]> {
  
  const res = await fetch(`${API_BASE_URL}/course/list`);
  if (!res.ok) throw new Error("Erro ao buscar matérias");
  return await res.json();
}

async function addSubject(title: string, file: File): Promise<any> {
  const formData = new FormData();
  formData.append("message", title); // nome da materia
  formData.append("files", file);   // arquivo
  const res = await fetch(`${API_BASE_URL}/course/ai`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Erro ao adicionar matéria");
  return await res.json();
}

async function deleteSubject(id: string) {
  const res = await fetch(`${API_BASE_URL}/subjects/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Erro ao remover matéria");
}

export default function SubjectsSection() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  // const [newSubject, setNewSubject] = useState("");
  const [adding, setAdding] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);

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
      .catch(() => setSubjects([]))
      .finally(() => setLoading(false));
  }, []);

  const handleToggle = (id: string) => {
    setSubjects((prev) =>
      prev.map((s) =>
        s.id === id ? { ...s, expanded: !s.expanded } : s
      )
    );
  };


  // const handleAddSubject = async (title: string, file: File | null) => {
  //   if (!newSubject.trim()) return;
  //   setAdding(true);
  //   try {
  //     const created = await addSubject(newSubject.trim(), file!);
  //     // Normalize the created subject to ensure id and title are present
  //     const normalized = {
  //       ...created,
  //       id: created.id || created.uuid || '',
  //       title: created.title || created.name || newSubject.trim(),
  //       color: getRandomSubjectColor(),
  //       expanded: true,
  //     };
  //     setSubjects((prev) => [
  //       ...prev,
  //       normalized,
  //     ]);
  //     setNewSubject("");
  //   } finally {
  //     setAdding(false);
  //   }
  // };


  const handleDelete = async (id: string) => {
    await deleteSubject(id);
    setSubjects((prev) => prev.filter((s) => s.id !== id));
  };

  // New handler for dialog submit
  const handleDialogSubmit = async (title: string, file: File | null) => {
    if (!title || !file) return;
    setAdding(true);
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
      setSubjects((prev) => [
        ...prev,
        normalized,
      ]);
      setDialogOpen(false);
    } finally {
      setAdding(false);
    }
  };

  return (
    <Box sx={{ p: 2, height: "100%", overflowY: "auto" }} className="custom-scrollbar">
      <Typography variant="h6" sx={{ mb: 2 }}>
        Matérias
      </Typography>
      {loading ? (
        <Typography>Carregando...</Typography>
      ) : (
        subjects.map((subject) => (
          <Paper

            key={subject.id} // use id as key


            sx={{
              mb: 2,
              p: 1.5,
              bgcolor: subject.color || subjectColors[subject.title] || "#bdbdbd",
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