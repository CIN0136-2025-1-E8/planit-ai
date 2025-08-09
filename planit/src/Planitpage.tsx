// import type React from "react"
import logo from './assets/logo.png'; 
// import { useState, useEffect } from "react"
import { useState } from "react"
import {
  Box,
  Paper,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Avatar,
} from "@mui/material"
import {
  Person as PersonIcon,
  CalendarMonth as CalendarIcon,
  Chat as ChatIcon,
  Description as FileIcon,
} from "@mui/icons-material"
//calendario
import Schedule from './calendar/Calendar'
//sessoes da sidebar
import ChatContainer from "./sidebar/chat/ChatContainer"
import SubjectsSection from "./sidebar/subjects/SubjectsSection"
import ProfileSection from "./sidebar/profile/ProfileSection"

// Criando o tema da página
const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#e91e63",
    },
    background: {
      default: "#f5f5f5",
      paper: "#ffffff",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
})

export default function PlanitPage() {
  // const [activeSection, setActiveSection] = useState<"profile" | "events" | "chat" | "subjects">("chat");
  const [activeSection, setActiveSection] = useState<"profile" | "chat" | "subjects">("chat");
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleCalendarUpdate = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: "flex", width: "100vw", height: "100vh", margin: 0, padding: 0, position: "fixed", left: 0, top: 0 }}>
        {/* Sidebar flush left, always full height */}
        <Paper
          elevation={0}
          sx={{
            width: 320,
            height: "100vh",
            bgcolor: "#f0f0f0",
            display: "flex",
            flexDirection: "column",
            borderRadius: 0,
            boxShadow: "none",
            margin: 0,
            padding: 0,
            position: "relative"
          }}
        >
          {/* Icones do topo da sidebar */}
          <Box sx={{ p: 2, display: "flex", gap: 1.5 }}>
              <img src={logo} alt="Planit Logo" style={{ height: 55, marginRight: 20 }} />

            <Avatar sx={{ bgcolor: "#e91e63", cursor: 'pointer' }} onClick={() => setActiveSection("profile")}>
              <PersonIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#ff9800", cursor: 'pointer' }}>
              <CalendarIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#4caf50", cursor: 'pointer' }} onClick={() => setActiveSection("chat")}>
              <ChatIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#9c27b0", cursor: 'pointer' }} onClick={() => setActiveSection("subjects")}>
              <FileIcon />
            </Avatar>
          </Box>
          <Box
            sx={{
              flex: 1,
              minHeight: 0, // Importante para scroll funcionar!
              overflow: "hidden", // Evita overflow externo
              display: "flex",
              flexDirection: "column",
            }}
          >
            {activeSection === "chat" && <ChatContainer onCalendarUpdate={handleCalendarUpdate} />}
            {activeSection === "profile" && <ProfileSection />}
            {/*{activeSection === "events" && <CalendarSection />}*/}
            {activeSection === "subjects" && <SubjectsSection onCalendarUpdate={handleCalendarUpdate} />}
          </Box>
        </Paper>
        {/* Main content area with blue background, fills remaining space, no borders */}
        <Box sx={{ flex: 1, height: "100vh", bgcolor: "#040032", margin: 0, padding: 0, border: 0 }}>
          <Schedule refreshTrigger={refreshTrigger} />
        </Box>
      </Box>
    </ThemeProvider>
  )
}
