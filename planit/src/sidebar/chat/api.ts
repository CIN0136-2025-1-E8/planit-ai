export async function sendMessageToBackend(message: string): Promise<string> {
  const formData = new FormData();
  formData.append("message", message);

  const response = await fetch("http://localhost:8000/chat/message", {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Erro ao enviar mensagem");
  return await response.text();
}


export async function fetchChatHistory(): Promise<{ role: "user" | "assistant"; text: string }[]> {
  const response = await fetch("http://localhost:8000/chat/history");
  if (!response.ok) throw new Error("Erro ao buscar histórico do chat");
  return await response.json();
}