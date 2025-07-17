import React, { useState, useEffect } from 'react';
import { format, addDays, subDays, startOfWeek, endOfWeek } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import ScheduleStyles from './calendarStyles';
import ClockIcon from './ClockIcon';
import { dateToGridRow, filterEventsByDay } from './CalendarUtils';

const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
const timeLabels = ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm'];

const Schedule = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
    const weekEnd = endOfWeek(currentDate, { weekStartsOn: 1 });

    // Placeholder for future backend integration
    fetchEventsForWeek(weekStart, weekEnd).then(fetchedEvents => {
      setEvents(fetchedEvents);
    });
  }, [currentDate]);

  const fetchEventsForWeek = async (weekStart: Date, weekEnd: Date) => {
    // Simulated fetch function - replace with real data fetching logic
    return new Promise(resolve => {
      setTimeout(() => {
        resolve([
          {
            id: 1,
            name: 'Evento 1',
            start: new Date(weekStart.getTime() + 2 * 24 * 60 * 60 * 1000 + 9 * 60 * 60 * 1000),
            end: new Date(weekStart.getTime() + 2 * 24 * 60 * 60 * 1000 + 10 * 60 * 60 * 1000),
            color: '#E69C5C',
            isLoading: false,
            details: 'Detalhes do Evento 1',
          },
          {
            id: 2,
            name: 'Evento 2',
            start: new Date(weekStart.getTime() + 4 * 24 * 60 * 60 * 1000 + 11 * 60 * 60 * 1000),
            end: new Date(weekStart.getTime() + 4 * 24 * 60 * 60 * 1000 + 12 * 60 * 60 * 1000),
            color: '#D9D9D9',
            isLoading: false,
            details: 'Detalhes do Evento 2',
          },
        ]);
      }, 1000);
    });
  };

  const handlePrevWeek = () => setCurrentDate(subDays(currentDate, 7));
  const handleNextWeek = () => setCurrentDate(addDays(currentDate, 7));

  const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(currentDate, { weekStartsOn: 1 });
  const weekEventsByDay = weekDays.map((_, dayIndex) => filterEventsByDay(events, dayIndex));

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
        </div>
      </div>
    </>
  );
};

export default Schedule;