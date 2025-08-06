import type {ChatFile} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export async function sendMessageToBackend(message: string, files: File[]): Promise<string> {
  const formData = new FormData();
  formData.append("message", message);

  files.forEach(file => {
    formData.append("files", file);
  });

  const response = await fetch(`${API_BASE_URL}/api/chat/message`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Erro ao enviar mensagem");
  return await response.json();
}

export async function fetchChatHistory(): Promise<{
  role: "user" | "assistant";
  text: string;
  files: ChatFile[] | null
}[]> {
  const response = await fetch(`${API_BASE_URL}/api/chat/history`);
  if (!response.ok) throw new Error("Erro ao buscar histórico do chat");
  return await response.json();
}
