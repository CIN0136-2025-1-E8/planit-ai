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
  const adjustTimeByHours = (datetime: string, hours: number) => {
    const date = new Date(datetime);
    date.setHours(date.getHours() + hours);
    return date.toISOString();
  };

  const response = await fetch(
    `${API_BASE_URL}/api/user/schedule?start_date=${encodeURIComponent(startDate)}&days=${days}&timezone=${encodeURIComponent(timezone)}`,
    {headers}
  );
  if (!response.ok) throw new Error("Error fetching schedule");
  const data = await response.json();

  // Adjust times in the fetched data
  const adjustedData = Object.fromEntries(
    Object.entries(data).map(([date, items]) => [
      date,
      (items as any[]).map((item: any) => ({
        ...item,
        start_datetime: adjustTimeByHours(item.start_datetime, 3),
        end_datetime: adjustTimeByHours(item.end_datetime, 3),
      })),
    ])
  );

  console.debug("fetchSchedule return (adjusted):", adjustedData); // Debug print
  return adjustedData;
}
