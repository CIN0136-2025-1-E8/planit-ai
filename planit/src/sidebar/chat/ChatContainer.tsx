import {useEffect, useRef, useState} from "react";
import ChatSection from "./ChatSection";
import type {Message} from "./types";
import {fetchChatHistory, sendMessageToBackend} from "./api";

const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "application/javascript",
  "text/javascript",
  "application/x-python-code",
  "text/x-python",
  "text/plain",
  "text/html",
  "text/css",
  "text/markdown",
  "text/csv",
  "text/xml",
  "application/rtf",
  "image/png",
  "image/jpeg",
  "image/webp",
  "image/heic",
  "image/heif",
];
const MAX_FILE_COUNT = 10;


export default function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [filesToSend, setFilesToSend] = useState<File[]>([]);
  const [fileError, setFileError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    fetchChatHistory()
      .then((history) =>
        setMessages(
          history.map((msg, idx) => ({
            id: String(idx),
            // role: msg.role === "model" ? "assistant" : "user",
            role: (msg.role as "model" | "user") === "model" ? "assistant" : "user",
            content: msg.text,
            files: msg.files || [],
          }))
        )
      )
      .catch(() => {
        // fallback: show initial assistant message if history fails
        setMessages([
          {
            id: "initial",
            role: "assistant",
            content:
              "Bom dia! Meu nome é Planit AI e estou aqui para lhe ajudar em sua organização de estudos! Já fiz um design inicial do seu cronograma de acordo com suas matérias, há alguma alteração que você gostaria de fazer?",
          },
        ]);
      });
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({behavior: "smooth"});
    }
  }, [messages, isLoading]);


  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      const validFiles: File[] = [];
      let error = null;

      if (filesToSend.length + selectedFiles.length > MAX_FILE_COUNT) {
        error = `Você pode selecionar no máximo ${MAX_FILE_COUNT} arquivos.`;
      } else {
        selectedFiles.forEach(file => {
          if (ALLOWED_FILE_TYPES.includes(file.type)) {
            validFiles.push(file);
          } else {
            error = `Tipo de arquivo não suportado: ${file.name}`;
          }
        });
      }

      if (error) {
        setFileError(error);
        setTimeout(() => setFileError(null), 5000);
      } else {
        setFilesToSend(prev => [...prev, ...validFiles]);
      }
    }
    if (e.target) e.target.value = '';
  };

  const handleAttachmentClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = (fileToRemove: File) => {
    setFilesToSend(prev => prev.filter(file => file !== fileToRemove));
  };


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      files: filesToSend.map(f => ({filename: f.name, mimetype: f.type}))
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setFilesToSend([]);
    setIsLoading(true);

    try {
      const response = await sendMessageToBackend(input, filesToSend);

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: response,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content:
            "Desculpe, tive um problema ao processar sua mensagem. Pode tentar novamente?",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <ChatSection
      messages={messages}
      input={input}
      isLoading={isLoading}
      messagesEndRef={messagesEndRef}
      handleSubmit={handleSubmit}
      setInput={setInput}
      filesToSend={filesToSend}
      handleAttachmentClick={handleAttachmentClick}
      handleFileChange={handleFileChange}
      handleRemoveFile={handleRemoveFile}
      fileInputRef={fileInputRef}
      fileError={fileError}
      setFileError={setFileError}
    />
  );
}