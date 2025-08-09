import {auth} from '../firebase-config';

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
    'Content-Type': 'application/json'
  };
}

export async function fetchSchedule(startDate: string, days: number, timezone: string) {
  const headers = await getAuthHeaders();
  const response = await fetch(
    `${API_BASE_URL}/api/user/schedule?start_date=${encodeURIComponent(startDate)}&days=${days}&timezone=${encodeURIComponent(timezone)}`,
    {headers}
  );
  if (!response.ok) throw new Error("Error fetching schedule");
    return await response.json();
}
