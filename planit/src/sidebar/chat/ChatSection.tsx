import {Box, Paper, Typography, TextField, IconButton} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import ReactMarkdown from "react-markdown";
import type {Components, ExtraProps} from "react-markdown";
import type {ReactNode} from "react";

interface CustomCodeProps extends ExtraProps {
  inline?: boolean;
  className?: string;
  children?: ReactNode;
}

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type ChatSectionProps = {
  messages: Message[];
  input: string;
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
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
  const markdownComponents: Components = {
    p: ({node, ...props}) => <Typography variant="body2" paragraph {...props} />,
    ul: ({node, ...props}) => <Typography component="ul" variant="body2" sx={{mt: 0, pl: "20px"}} {...props} />,
    ol: ({node, ...props}) => <Typography component="ol" variant="body2" sx={{mt: 0, pl: "20px"}} {...props} />,
    li: ({node, ...props}) => (
      <li>
        <Typography component="span" variant="body2" {...props} />
      </li>
    ),
    pre: ({node, ...props}) => (
      <Box
        component="pre"
        sx={{
          bgcolor: "#bdbdbd",
          color: "#212121",
          p: 1.5,
          borderRadius: 1,
          overflowX: "auto",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
        {...props}
      />
    ),
    code: ({node, inline, className, children, ...props}: CustomCodeProps) => {
      if (inline) {
        return (
          <Box
            component="code"
            sx={{
              bgcolor: "#bdbdbd",
              color: "#212121",
              px: "5px",
              py: "2px",
              borderRadius: 1,
              fontFamily: "monospace",
              fontSize: "0.825rem",
            }}
            {...props}
          >
            {children}
          </Box>
        );
      }
      return (
        <Box
          component="code"
          sx={{fontFamily: "monospace", fontSize: "0.875rem"}}
          className={className}
          {...props}
        >
          {children}
        </Box>
      );
    },
    blockquote: ({node, ...props}) => (
      <Box
        component="blockquote"
        sx={{
          borderLeft: "4px solid #bdbdbd",
          color: "#424242",
          pl: 2,
          my: 1.5,
          fontStyle: "italic",
        }}
        {...props}
      />
    ),
    hr: ({node, ...props}) => (
      <hr style={{border: 0, borderTop: "1px solid #bdbdbd", margin: "1em 0"}} {...props} />
    ),
  };

  const userPaperSx = {
    alignSelf: "flex-end",
    bgcolor: "#1976d2",
    color: "white",
    borderRadius: "16px 16px 4px 16px",
    "& a": {color: "#b3e5fc", textDecoration: "underline"},
  };

  const assistantPaperSx = {
    alignSelf: "flex-start",
    bgcolor: "#e0e0e0",
    color: "#212121",
    borderRadius: "16px 16px 16px 4px",
    "& a": {color: "#1976d2", textDecoration: "underline"},
    "& p:first-of-type, & ul:first-of-type, & ol:first-of-type, & pre:first-of-type, & blockquote:first-of-type, & hr:first-of-type":
      {
        marginTop: 0,
      },
    "& p:last-of-type, & ul:last-of-type, & ol:last-of-type, & pre:last-of-type, & blockquote:last-of-type, & hr:last-of-type":
      {
        marginBottom: 0,
      },
  };

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
              wordBreak: "break-word",
              ...(message.role === "user" ? userPaperSx : assistantPaperSx),
            }}
          >
            {message.role === "assistant" ? (
              <ReactMarkdown components={markdownComponents}>{message.content}</ReactMarkdown>
            ) : (
              <Typography variant="body2" sx={{whiteSpace: "pre-wrap"}}>
                {message.content}
              </Typography>
            )}
          </Paper>
        ))}
        {isLoading && (
          <Paper
            elevation={0}
            sx={{
              p: 2,
              maxWidth: "80%",
              alignSelf: "flex-start",
              bgcolor: "#e0e0e0",
              color: "#212121",
              borderRadius: "16px 16px 16px 4px",
            }}
          >
            <Typography variant="body2">Digitando...</Typography>
          </Paper>
        )}
        <div ref={messagesEndRef}/>
      </Box>
      {/* Input do chat */}
      <Box sx={{p: 2}}>
        <form onSubmit={handleSubmit} style={{display: "flex", gap: 8}}>
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
                "& fieldset": {border: "none"},
                "&:hover fieldset": {border: "none"},
                "&.Mui-focused fieldset": {border: "none"},
              },
            }}
          />
          <IconButton
            type="submit"
            color="primary"
            disabled={isLoading}
            sx={{bgcolor: "#1976d2", color: "white", "&:hover": {bgcolor: "#1565c0"}}}
          >
            <SendIcon/>
          </IconButton>
        </form>
      </Box>
    </>
  );
}