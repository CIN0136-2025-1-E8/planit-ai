import React from "react";
import { Box, Paper, Typography, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type ChatSectionProps = {
  messages: Message[];
  input: string;
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement>;
  handleSubmit: (e: React.FormEvent) => void;
  setInput: React.Dispatch<React.SetStateAction<string>>;
};

export default function ChatSection({
  messages,
  input,
  isLoading,
  messagesEndRef,
  handleSubmit,
  setInput,
}: ChatSectionProps) {
  return (
    <>
      {/* Mensagens do chat */}
      <Box
        className="custom-scrollbar"
        sx={{
          flex: 1,
          minHeight: 0,
          p: 2,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
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
      {/* Input do chat */}
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
                "& fieldset": { border: "none" },
                "&:hover fieldset": { border: "none" },
                "&.Mui-focused fieldset": { border: "none" },
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
    </>
  );
}