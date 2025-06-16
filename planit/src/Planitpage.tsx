import type React from "react"
import logo from './assets/logo.png'; 
import { useState, useEffect, useRef } from "react"
import {
  Box,
  TextField,
  Paper,
  Typography,
  ThemeProvider,
  createTheme,
  CssBaseline,
  IconButton,
  Avatar,
} from "@mui/material"
import {
  Send as SendIcon,
  Person as PersonIcon,
  CalendarMonth as CalendarIcon,
  Chat as ChatIcon,
  Description as FileIcon,
  Public as GlobeIcon,
} from "@mui/icons-material"

async function sendMessageToBackend(sessionId: string, message: string): Promise<string> {
  const response = await fetch("http://localhost:8000/chat/message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!response.ok) throw new Error("Erro ao enviar mensagem");
  const data = await response.json();
  return data.reply;
}



type Message = {
  id: string
  role: "user" | "assistant"
  content: string
}

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
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setMessages([
      {
        id: "initial",
        role: "assistant",
        content:
          "Bom dia! Meu nome é Planit AI e estou aqui para lhe ajudar em sua organização de estudos! Já fiz um design inicial do seu cronograma de acordo com suas matérias, há alguma alteração que você gostaria de fazer?",
      },
    ])
  }, [])

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages, isLoading])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const sessionId = "demo-session";
      const response = await sendMessageToBackend(sessionId, input);

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: response,
        },
      ]);
    } catch (error) {
      console.error("Error getting response:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "Desculpe, tive um problema ao processar sua mensagem. Pode tentar novamente?",
        },
      ]);
    } finally {
      setIsLoading(false)
    }
  } 
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: "flex", height: "100vh", bgcolor: "background.default" }}>
        {/*sidebar com o chat*/}
        <Paper
          elevation={0}
          sx={{
            width: 320,
            bgcolor: "#f0f0f0",
            display: "flex",
            flexDirection: "column",
            borderRadius: 0,
          }}
        >
          {/* Icons */}
          <Box sx={{ p: 2, display: "flex", gap: 1.5 }}>
              <img src={logo} alt="Planit Logo" style={{ height: 55, marginRight: 20 }} />
          
            <Avatar sx={{ bgcolor: "#e91e63" }}>
              <PersonIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#ff9800" }}>
              <CalendarIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#4caf50" }}>
              <ChatIcon />
            </Avatar>
            <Avatar sx={{ bgcolor: "#9c27b0" }}>
              <FileIcon />
            </Avatar>
          </Box>

          {/* Chat Messages */}
          <Box
            sx={{
              flex: 1,
              p: 2,
              overflowY: "auto",
              display: "flex",
              flexDirection: "column",
              gap: 2,
            }}
          >
            {/* Display all messages */}
            {messages.map((message) => (
              <Paper
                key={message.id}
                elevation={0}
                sx={{
                  p: 2,
                  maxWidth: "80%",
                  alignSelf: message.role === "user" ? "flex-end" : "flex-start",
                  bgcolor: message.role === "user" ? "#1976d2" : "#e91e63",
                  color: "white",
                  borderRadius: message.role === "user" ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                }}
              >
                <Typography variant="body2">{message.content}</Typography>
              </Paper>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  maxWidth: "80%",
                  alignSelf: "flex-start",
                  bgcolor: "#e91e63",
                  color: "white",
                  borderRadius: "16px 16px 16px 4px",
                }}
              >
                <Typography variant="body2">Digitando...</Typography>
              </Paper>
            )}
            <div ref={messagesEndRef} />
          </Box>

          {/* Chat Input */}
          <Box sx={{ p: 2 }}>
            <form onSubmit={handleSubmit} style={{ display: "flex", gap: 8 }}>
              <TextField
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Digite sua mensagem..."
                fullWidth
                variant="outlined"
                size="small"
                disabled={isLoading}
                sx={{
                  "& .MuiOutlinedInput-root": {
                    bgcolor: "#d3d3d3",
                    "& fieldset": {
                      border: "none",
                    },
                    "&:hover fieldset": {
                      border: "none",
                    },
                    "&.Mui-focused fieldset": {
                      border: "none",
                    },
                  },
                }}
              />
              <IconButton
                type="submit"
                color="primary"
                disabled={isLoading}
                sx={{ bgcolor: "#1976d2", color: "white", "&:hover": { bgcolor: "#1565c0" } }}
              >
                <SendIcon />
              </IconButton>
            </form>
          </Box>
        </Paper>

   
            
          
        
      </Box>
    </ThemeProvider>
  )
}
