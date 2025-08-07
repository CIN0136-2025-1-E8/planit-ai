import React, { useState, useEffect } from 'react';
import { format, addDays, subDays, startOfWeek, endOfWeek } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import ScheduleStyles from './calendarStyles';
import ClockIcon from './ClockIcon';
import { fetchSchedule } from './api';

const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
const timeLabels = ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm'];

const Schedule = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [schedule, setSchedule] = useState({});
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  useEffect(() => {
    const startDate = format(startOfWeek(currentDate, { weekStartsOn: 1 }), 'yyyy-MM-dd');
    fetchSchedule(startDate, 7, timezone)
      .then((data) => setSchedule(data))
      .catch((error) => console.error(error));
  }, [currentDate]);

  const handlePrevWeek = () => setCurrentDate(subDays(currentDate, 7));
  const handleNextWeek = () => setCurrentDate(addDays(currentDate, 7));

  const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(currentDate, { weekStartsOn: 1 });

  const calculateGridRow = (datetime: Date) => {
    const hours = datetime.getHours();
    const minutes = datetime.getMinutes();
    return Math.floor((hours - 8) * 2 + 2 + (minutes / 30)); // Adjust for 30-minute intervals starting at 8am
  };

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

          {Object.entries(schedule).flatMap(([date, items]) =>
            (items as any[]).map((item) => {
              const dayOfWeek = new Date(date).getDay();
              const startRow = calculateGridRow(new Date(item.start_datetime));
              const endRow = calculateGridRow(new Date(item.end_datetime));
              return (
                <div
                  key={item.uuid}
                  className="event-item"
                  style={{
                    gridColumn: dayOfWeek + 2,
                    gridRow: `${startRow} / ${endRow}`,
                    backgroundColor: item.item_type === 'event' ? '#E68C8C' : '#8CB9E6',
                  }}
                >
                  <div className="event-header">
                    <ClockIcon />
                    <span
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        maxWidth: '100%',
                      }}
                    >
                      {item.course_title && (
                        <span
                          style={{
                            fontSize: '0.85em',
                            fontWeight: 'normal',
                            color: '#333',
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'normal',
                            marginBottom: '2px',
                          }}
                        >
                          {item.course_title}
                        </span>
                      )}
                      <span
                        style={{
                          fontSize: '1em',
                          fontWeight: 'bold',
                          color: '#222',
                          wordBreak: 'break-word',
                        }}
                      >
                        {item.title}
                      </span>
                    </span>
                  </div>
                  {item.description && <div className="event-details">{item.description}</div>}
                </div>
              );
            })
          )}
        </div>
      </div>
    </>
  );
};

export default Schedule;