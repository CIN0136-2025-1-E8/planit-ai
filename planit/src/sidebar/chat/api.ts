import {auth} from '../../firebase-config';
import type {ChatFile} from "./types";

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

async function getAuthHeaders() {
  await auth.authStateReady();
  const user = auth.currentUser;

  if (!user) {
    throw new Error("Usuário não autenticado. Por favor, faça login novamente.");
  }

  const token = await user.getIdToken();
  return {
    'Authorization': `Bearer ${token}`,
  };
}

export async function sendMessageToBackend(message: string, files: File[]): Promise<string> {
  const headers = await getAuthHeaders();

  const formData = new FormData();
  formData.append("message", message);

  files.forEach(file => {
    formData.append("files", file);
  });

  const response = await fetch(`${API_BASE_URL}/api/chat/message`, {
    method: "POST",
    headers: {
      ...headers,
    },
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.text();
    throw new Error(errorData || "Erro ao enviar mensagem");
  }

  const responseText = await response.text();
  try {
    const jsonResponse = JSON.parse(responseText);
    return jsonResponse.response || jsonResponse;
  } catch (e) {
    return responseText;
  }
}

export async function fetchChatHistory(): Promise<{
  role: "user" | "assistant";
  text: string;
  files: ChatFile[] | null
}[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(`${API_BASE_URL}/api/chat/history`, {
    headers: {
      ...headers,
      'Content-Type': 'application/json',
    }
  });

  if (!response.ok) {
    console.error("Erro ao buscar histórico do chat:", response.statusText);
    throw new Error("Não foi possível carregar o histórico do chat.");
  }
  return await response.json();
}
