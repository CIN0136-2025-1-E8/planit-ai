import { useState, useEffect, useRef } from "react";
import ChatSection from "./ChatSection";
import type { Message } from "./types";
import { sendMessageToBackend, fetchChatHistory } from "./api";

export default function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch chat history on mount
  useEffect(() => {
    fetchChatHistory()
      .then((history) =>
        setMessages(
          history.map((msg, idx) => ({
            id: String(idx),
            role: msg.role === "model" ? "assistant" : "user",
            content: msg.text,
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
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await sendMessageToBackend(input);

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
    />
  );
}
