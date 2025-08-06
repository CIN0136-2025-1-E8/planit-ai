import {Alert, Box, Chip, Collapse, IconButton, Paper, TextField, Typography} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import AttachmentIcon from "@mui/icons-material/Attachment";
import CloseIcon from '@mui/icons-material/Close';
import DoNotDisturbOnIcon from '@mui/icons-material/DoNotDisturbOn';
import type {Components, ExtraProps} from "react-markdown";
import ReactMarkdown from "react-markdown";
import type {ReactNode} from "react";
import React, {useEffect, useRef} from "react";
import type {Message} from "./types";


interface CustomCodeProps extends ExtraProps {
  inline?: boolean;
  className?: string;
  children?: ReactNode;
}

type ChatSectionProps = {
  messages: Message[];
  input: string;
  isLoading: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
  handleSubmit: (e: React.FormEvent) => void;
  setInput: React.Dispatch<React.SetStateAction<string>>;
  filesToSend: File[];
  handleAttachmentClick: () => void;
  handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleRemoveFile: (file: File) => void;
  fileInputRef: React.RefObject<HTMLInputElement | null>;
  fileError: string | null;
  setFileError: React.Dispatch<React.SetStateAction<string | null>>;
};

export default function ChatSection({
                                      messages,
                                      input,
                                      isLoading,
                                      messagesEndRef,
                                      handleSubmit,
                                      setInput,
                                      filesToSend,
                                      handleAttachmentClick,
                                      handleFileChange,
                                      handleRemoveFile,
                                      fileInputRef,
                                      fileError,
                                      setFileError,
                                    }: ChatSectionProps) {
  const fileListBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fileListBox = fileListBoxRef.current;
    if (fileListBox) {
      const handleWheel = (e: WheelEvent) => {
        if (fileListBox.scrollWidth > fileListBox.clientWidth) {
          e.preventDefault();
          fileListBox.scrollLeft += e.deltaY;
        }
      };
      fileListBox.addEventListener('wheel', handleWheel, {passive: false});

      return () => {
        fileListBox.removeEventListener('wheel', handleWheel);
      };
    }
  }, [filesToSend]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

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
          <Box key={message.id} sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: message.role === 'user' ? 'flex-end' : 'flex-start'
          }}>
            {message.files && message.files.length > 0 && (
              <Box sx={{display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 0.5, maxWidth: '80%'}}>
                {message.files.map((file, index) => (
                  <Chip key={index} label={file.filename} size="small"/>
                ))}
              </Box>
            )}
            <Paper
              elevation={0}
              sx={{
                p: 2,
                maxWidth: "95%",
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
          </Box>
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

      <Box sx={{p: 2, borderTop: '1px solid #e0e0e0'}}>
        <Collapse in={!!fileError}>
          <Alert
            severity="info"
            icon={<DoNotDisturbOnIcon sx={{color: 'error.main'}}/>}
            sx={{
              mb: 1,
              bgcolor: 'transparent',
              color: 'text.secondary',
              borderColor: 'error.main',
              borderWidth: '2px',
              borderStyle: 'solid',
              alignItems: 'center',
            }}
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  setFileError(null);
                }}
              >
                <CloseIcon fontSize="inherit"/>
              </IconButton>
            }
          >
            {fileError}
          </Alert>
        </Collapse>

        {filesToSend.length > 0 && (
          <Box ref={fileListBoxRef} sx={{mb: 1, display: 'flex', gap: 1, overflowX: 'auto', pb: 1}}
               className="custom-scrollbar">
            {filesToSend.map((file, index) => (
              <Chip
                key={index}
                label={file.name}
                onDelete={() => handleRemoveFile(file)}
              />
            ))}
          </Box>
        )}

        <form onSubmit={handleSubmit} style={{display: "flex", gap: 8, alignItems: 'flex-end'}}>
          <input
            type="file"
            multiple
            hidden
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="application/pdf,application/javascript,text/javascript,application/x-python-code,text/x-python,text/plain,text/html,text/css,text/markdown,text/csv,text/xml,application/rtf,image/png,image/jpeg,image/webp,image/heic,image/heif"
          />
          <IconButton
            type="button"
            onClick={handleAttachmentClick}
            disabled={isLoading}
            sx={{flexShrink: 0}}
          >
            <AttachmentIcon/>
          </IconButton>
          <TextField
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Digite aqui..."
            fullWidth
            variant="outlined"
            size="small"
            disabled={isLoading}
            multiline
            minRows={1}
            maxRows={3}
            onKeyDown={handleKeyDown}
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
            disabled={isLoading || !input.trim()}
            sx={{bgcolor: "#1976d2", color: "white", "&:hover": {bgcolor: "#1565c0"}, flexShrink: 0}}
          >
            <SendIcon/>
          </IconButton>
        </form>
      </Box>
    </>
  );
}