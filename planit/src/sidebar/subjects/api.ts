import {auth} from '../../firebase-config';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

async function getAuthHeaders() {
  await auth.authStateReady();
  const user = auth.currentUser;
  if (!user) {
    throw new Error("Usuário não autenticado.");
  }
  const token = await user.getIdToken();
  return {
    'Authorization': `Bearer ${token}`,
  };
}

export type Subject = {
  id: string;
  title: string;
  color: string;
  files: { name: string; url: string }[];
  expanded?: boolean;
};


export async function fetchSubjects(): Promise<Subject[]> {
  const headers = await getAuthHeaders();
  const res = await fetch(`${API_BASE_URL}/api/course/list`, {headers});
  if (!res.ok) throw new Error("Erro ao buscar matérias");
  return await res.json();
}

export async function addSubject(title: string, file: File): Promise<any> {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("message", title);
  formData.append("files", file);
  const res = await fetch(`${API_BASE_URL}/api/course/ai`, {
    method: "POST",
    headers: {...headers},
    body: formData,
  });
  if (!res.ok) throw new Error("Erro ao adicionar matéria");
  return await res.json();
}

export async function deleteSubject(id: string): Promise<void> {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("course_uuid", id);

  const res = await fetch(`${API_BASE_URL}/api/course/`, {
    method: "DELETE",
    headers: {...headers},
    body: formData,
  });
  if (!res.ok) throw new Error("Erro ao remover matéria");
}
