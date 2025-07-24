import React, { useState, useEffect } from 'react';
import { format, addDays, subDays, startOfWeek, endOfWeek } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import ScheduleStyles from './calendarStyles';
import ClockIcon from './ClockIcon';
import { dateToGridRow } from './CalendarUtils';
import { fetchEventsForNextWeek } from './api';

const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
const timeLabels = ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm'];

interface CalendarEvent {
  id: number;
  name: string;
  start: Date;
  end: Date;
  color?: string;
  isLoading?: boolean;
  details?: string | null;
}

const mockUser = {
  uuid: '11e75ac9-aa93-45ba-8637-8eb16ddedcb3', // Use a real or test user UUID
};

const Schedule = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  useEffect(() => {
    // Para DEMO: usar eventos mockados
    setEvents(mockEvents);
    // Para produção, descomente abaixo e remova a linha acima:
    // fetchEventsForNextWeek(mockUser.uuid).then(fetchedEvents => {
    //   const parsedEvents = fetchedEvents.map((event: any) => ({
    //     ...event,
    //     start: new Date(event.start),
    //     end: new Date(event.end),
    //   }));
    //   setEvents(parsedEvents);
    // }).catch(() => setEvents([]));
  }, [currentDate]);

  const handlePrevWeek = () => setCurrentDate(subDays(currentDate, 7));
  const handleNextWeek = () => setCurrentDate(addDays(currentDate, 7));

  const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(currentDate, { weekStartsOn: 1 });

  // MOCK EVENTS FOR DEMO (frontend only, recurring at class times)
  function getNextWeekdayDate(weekday: number, hour: number, minute: number) {
    const now = new Date();
    const result = new Date(now);
    const currentDay = now.getDay();
    // weekday: 1=Monday, 2=Tuesday, ..., 5=Friday
    let daysToAdd = (weekday + 7 - currentDay) % 7;
    if (daysToAdd === 0 && (now.getHours() > hour || (now.getHours() === hour && now.getMinutes() >= minute))) {
      daysToAdd = 7; // next week if time already passed today
    }
    result.setDate(now.getDate() + daysToAdd);
    result.setHours(hour, minute, 0, 0);
    return result;
  }

  const mockEvents = [
    // Arquitetura de Sistemas: Terça (2) e Quinta (4), 13h-15h
    {
      id: 1,
      name: "Arquitetura de Sistemas",
      start: getNextWeekdayDate(2, 13, 0),
      end: getNextWeekdayDate(2, 15, 0),
      color: "#ff9800",
      details: "Aula de Arquitetura de Sistemas (Terça)",
    },
    {
      id: 2,
      name: "Arquitetura de Sistemas",
      start: getNextWeekdayDate(4, 13, 0),
      end: getNextWeekdayDate(4, 15, 0),
      color: "#ff9800",
      details: "Aula de Arquitetura de Sistemas (Quinta)",
    },
    // IP: Sexta (5) 13h-17h, Segunda (1) 13h-15h
    {
      id: 3,
      name: "Introdução a Programação",
      start: getNextWeekdayDate(5, 13, 0),
      end: getNextWeekdayDate(5, 17, 0),
      color: "#4caf50",
      details: "Laboratório de Introdução a Programação (Sexta)",
    },
    {
      id: 4,
      name: "Introdução a Programação",
      start: getNextWeekdayDate(1, 13, 0),
      end: getNextWeekdayDate(1, 15, 0),
      color: "#4caf50",
      details: "Laboratório de Introdução a Programação (Segunda)",
    },
  ];

  return (
    <>
      <ScheduleStyles />
      <div className="schedule-wrapper">
        <header className="schedule-header">
          <h2>{`${format(weekStart, 'd MMM', { locale: ptBR })} - ${format(weekEnd, 'd MMM yyyy', { locale: ptBR })}`}</h2>
          <div className="nav-buttons">
            <button onClick={handlePrevWeek}>Anterior</button>
            <button onClick={handleNextWeek}>Próxima</button>
          </div>
        </header>

        {/* Vista Desktop */}
        <div className="schedule-container d-none d-md-grid" style={{ gridTemplateColumns: `60px repeat(7, 1fr)`, gridAutoRows: '30px', overflowY: 'auto', maxHeight: '100vh' }}>
          {weekDays.map((day, index) => (
            <div key={day} className="day-label" style={{ gridColumn: index + 2 }}>{day}</div>
          ))}
          
          {timeLabels.map((time, index) => (
            <React.Fragment key={time}>
              <div className="time-label" style={{ gridRow: index * 2 + 2 }}>{time}</div>
              <div className="grid-line" style={{ gridColumn: `2 / -1`, gridRow: index * 2 + 3 }}></div>
            </React.Fragment>
          ))}
          
          {events.map(event => {
            const dayOfWeek = new Date(event.start).getDay();
            return (
              <div
                key={event.id}
                className="event-item"
                style={{
                  gridColumn: dayOfWeek + 2,
                  gridRow: `${dateToGridRow(event.start)} / ${dateToGridRow(event.end)}`,
                  backgroundColor: event.color,
                }}
              >
                <div className="event-header">
                  <ClockIcon />
                  <span>{event.name}</span>
                </div>
                {event.isLoading && <div className="event-details">A carregar resumo...</div>}
                {event.details && <div className="event-details">{event.details}</div>}
                {!event.details && !event.isLoading && (
                  <button onClick={() => console.log('Load summary')}>Carregar Resumo</button>
                )}
              </div>
            );
          })}

          {/* Renderiza eventos mockados apenas na semana atual */}
          {format(weekStart, 'yyyy-MM-dd') === format(new Date(), 'yyyy-MM-dd') && mockEvents.map(event => {
            const dayOfWeek = new Date(event.start).getDay();
            return (
              <div
                key={event.id}
                className="event-item"
                style={{
                  gridColumn: dayOfWeek + 2,
                  gridRow: `${dateToGridRow(event.start)} / ${dateToGridRow(event.end)}`,
                  backgroundColor: event.color,
                }}
              >
                <div className="event-header">
                  <ClockIcon />
                  <span>{event.name}</span>
                </div>
                <div className="event-details">{event.details}</div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default Schedule;