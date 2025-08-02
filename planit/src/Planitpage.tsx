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
//sessoes da sidebar
import ChatContainer from "./sidebar/chat/ChatContainer"
import SubjectsSection from "./sidebar/subjects/SubjectsSection"

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
  const [activeSection, setActiveSection] = useState<"chat" | "subjects">("chat");

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: "flex", height: "100vh", bgcolor: "background.default" }}>
        {/*sidebar com o chat*/}
        <Paper
          elevation={0}
          sx={{
            width: 320,
            height: "100vh", // Garante altura total da tela
            bgcolor: "#f0f0f0",
            display: "flex",
            flexDirection: "column",
            borderRadius: 0,
          }}
        >
          {/* Icones do topo da sidebar */}
          <Box sx={{ p: 2, display: "flex", gap: 1.5 }}>
              <img src={logo} alt="Planit Logo" style={{ height: 55, marginRight: 20 }} />
          
            <Avatar sx={{ bgcolor: "#e91e63" }}>
              <PersonIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#ff9800" }}>
              <CalendarIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#4caf50" }} onClick={() => setActiveSection("chat")}>
              <ChatIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#9c27b0" }} onClick={() => setActiveSection("subjects")}>
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
            {activeSection === "chat" && <ChatContainer />}
            {/*{activeSection === "profile" && <ProfileSection />} */}
            {/*{activeSection === "events" && <CalendarSection />}*/}
            {activeSection === "subjects" && <SubjectsSection />}
          </Box>
        </Paper>

   
            
          
        
      </Box>
    </ThemeProvider>
  )
}
