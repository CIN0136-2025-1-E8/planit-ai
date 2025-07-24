export async function fetchEventsForNextWeek(owner_uuid: string) {
  const response = await fetch(`http://localhost:8000/events/next_week?owner_uuid=${encodeURIComponent(owner_uuid)}`);
  if (!response.ok) throw new Error("Erro ao buscar eventos da próxima semana");
  return await response.json();
}
